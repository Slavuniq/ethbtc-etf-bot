#!/usr/bin/env python3
"""Сканер цен и наличия SUP-досок до 150 EUR в магазинах района Ниццы.

Запускается в GitHub Actions: у раннера полный доступ в интернет,
в отличие от изолированного контейнера сессии.

Для каждой карточки товара снимаем:
  - цену (JSON-LD offers.price, затем видимый текст как запасной вариант)
  - наличие (schema.org availability + текстовые маркеры "rupture"/"epuise")
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field

from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

TARGETS = [
    ("LIDL", "Crivit polyvalent gonflable (315x84x15, 140 kg)",
     "https://www.lidl.fr/p/crivit-stand-up-paddle-polyvalent-gonflable/p100405281"),
    ("LIDL", "Crivit polyvalent basic",
     "https://www.lidl.fr/p/crivit-stand-up-paddle-gonflable-polyvalent-basic/p100388784"),
    ("LIDL", "Crivit polyvalent Aquaview",
     "https://www.lidl.fr/p/crivit-stand-up-paddle-gonflable-polyvalent-aquaview/p100405264"),
    ("LIDL", "Crivit polyvalent + pompe et pagaie",
     "https://www.lidl.fr/p/crivit-stand-up-paddle-polyvalent-gonflable-pompe-et-pagaie/p100405156"),
    ("GIFI", "Paddle gonflable 274x76x10",
     "https://www.gifi.fr/loisirs/sport/sport-individuel/paddle-gonflable-274x76xep10cm/000000000000617083.html"),
    ("GIFI", "Planche paddle gonflable 365x76x15",
     "https://www.gifi.fr/loisirs/sport/sport-individuel/planche-paddle-gonflable-1-personne-plastique-jaune-et-vert-365x76xep15cm/000000000000644661.html"),
    ("GIFI", "Planche paddle gonflable 320x81x15",
     "https://www.gifi.fr/loisirs/sport/sport-individuel/planche-paddle-gonflable-1-personne-motif-corail-jaune-et-bleu-320x81xep15cm/000000000000644662.html"),
    ("DECATHLON", "Itiwit x100 debutant 11 pieds (neuf, ориентир)",
     "https://www.decathlon.fr/p/stand-up-paddle-gonflable-debutant-11-pieds-bleu/_/R-p-303064"),
    ("DECATHLON", "Seconde Vie — stand up paddle occasion",
     "https://www.decathlon.fr/tous-les-sports/stand-up-paddle-sup/stand-up-paddle-de-seconde-vie"),
    ("DECATHLON", "Seconde Vie — liste materiel sports d'eau",
     "https://www.decathlon.fr/occasion/materiel-sports-d-eau-occasion"),
    ("CARREFOUR", "Bestway Hydro-Force Aqua Wander 305x84x12",
     "https://www.carrefour.fr/p/bestway-paddle-gonflable-hydro-force-aqua-wander-305-x-84-x-12-cm-6941607334188"),
    ("CARREFOUR", "Intex Aqua Quest 320",
     "https://www.carrefour.fr/p/intex-aqua-quest-320-planche-sup-6941057422817"),
    # дискаунтеры — магазины есть в Ницце и Сен-Лоран-дю-Вар
    ("STOKOMANI", "Paddle gonflable rouge",
     "https://www.stokomani.fr/paddle-gonflable-rouge.html"),
    ("STOKOMANI", "поиск: paddle",
     "https://www.stokomani.fr/catalogsearch/result/?q=paddle"),
    ("FOIR'FOUILLE", "поиск: paddle",
     "https://www.lafoirfouille.fr/catalogsearch/result/?q=paddle"),
    ("CENTRAKOR", "поиск: paddle",
     "https://www.centrakor.com/catalogsearch/result/?q=paddle"),
    ("ACTION", "Stand up paddle gonflable Q4Life",
     "https://shop.action.com/fr-be/p/8719407071897/stand-up-paddle-gonflable-q4life"),
    ("CDISCOUNT", "Bestway Aqua Journey SUP",
     "https://www.cdiscount.com/le-sport/surf-shop/bestway-paddle-aqua-journey-sup-avec-rame-et-acces/f-1213122-65302.html"),
    # б/у: Leboncoin по департаменту 06, потолок 130 EUR
    ("LEBONCOIN", "paddle, 06, <=130 EUR",
     "https://www.leboncoin.fr/recherche?text=paddle&locations=d_06&price=min-130"),
    ("LEBONCOIN", "paddle gonflable, 06",
     "https://www.leboncoin.fr/recherche?text=paddle%20gonflable&locations=d_06"),
    ("LEBONCOIN", "Itiwit б/у, вся Франция",
     "https://www.leboncoin.fr/recherche?text=itiwit&price=min-130"),
    ("CAMPSIDER", "paddle gonflable occasion",
     "https://campsider.com/sports-nautiques/equipement-paddle/paddle-gonflable-occasion"),
    # крупные сети — поиск по сайту
    ("E.LECLERC", "поиск: paddle gonflable",
     "https://www.e.leclerc/recherche?q=paddle+gonflable"),
    ("E.LECLERC", "раздел: planche de paddle",
     "https://www.e.leclerc/cat/planche-de-paddle"),
    ("E.LECLERC", "раздел: stand-up paddle",
     "https://www.e.leclerc/cat/paddle"),
    ("INTERMARCHE", "поиск: paddle",
     "https://www.intermarche.com/recherche?q=paddle"),
    ("AUCHAN", "поиск: paddle gonflable",
     "https://www.auchan.fr/recherche?text=paddle+gonflable"),
    ("SUPER U", "поиск: paddle",
     "https://www.coursesu.com/recherche?q=paddle"),
    ("MONOPRIX", "поиск: paddle",
     "https://www.monoprix.fr/courses/recherche?q=paddle"),
    ("CORA", "поиск: paddle",
     "https://www.cora.fr/recherche?q=paddle"),
    ("ALDI", "поиск: paddle",
     "https://www.aldi.fr/resultats-de-recherche.html?q=paddle"),
    # агрегаторы цен — ловят скидки по всем продавцам сразу
    ("IDEALO", "SUP до 100 EUR",
     "https://www.idealo.fr/cat/28644F7420876/stand-up-paddle.html?max=100"),
    ("IDEALO", "SUP, сортировка по цене",
     "https://www.idealo.fr/cat/28644/stand-up-paddle.html?sortKey=minPrice"),
    # проверка скидки -25% на Crivit polyvalent: источники, где она была заявлена
    ("PROMO-123", "Crivit polyvalent -25%",
     "https://www.123catalogue.fr/catalogue/lidl/crivit-stand-up-paddle-polyvalent-gonflable-695260"),
    ("PROMO-123", "Stand Up Paddle Polyvalent",
     "https://www.123catalogue.fr/catalogue/lidl/stand-up-paddle-polyvalent-gonflable-328850"),
    ("PROMO-123", "Stand Up Paddle Gonflable",
     "https://www.123catalogue.fr/catalogue/lidl/stand-up-paddle-gonflable-284699"),
    ("PROMOCATALOGUES", "Crivit chez Lidl",
     "https://www.promocatalogues.fr/offres/crivit/lidl"),
    ("PROMOS.FR", "Crivit polyvalent (акция 79 EUR)",
     "https://www.promos.fr/lidl/crivit-stand-up-paddle-polyvalent-gonflable-a-79eur-932436"),
]

PRICE_RE = re.compile(r"(\d{1,4}[.,]\d{2})\s*(?:€|EUR)|(?:€|EUR)\s*(\d{1,4}[.,]\d{2})")
OOS_RE = re.compile(r"rupture|épuisé|epuise|indisponible|out of stock|sold\s*out", re.I)
INSTOCK_RE = re.compile(r"ajouter au panier|add to cart|en stock|disponible", re.I)


@dataclass
class Result:
    store: str
    name: str
    url: str
    status: str = "?"
    jsonld_price: str = ""
    jsonld_avail: str = ""
    text_prices: list = field(default_factory=list)
    signals: list = field(default_factory=list)
    error: str = ""


def parse_jsonld(page) -> tuple[str, str]:
    """Достаёт price / availability из любого блока schema.org Product."""
    price = avail = ""
    for handle in page.query_selector_all('script[type="application/ld+json"]'):
        raw = handle.inner_text() or ""
        try:
            data = json.loads(raw)
        except Exception:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
                continue
            if not isinstance(node, dict):
                continue
            offers = node.get("offers")
            if offers:
                stack.append(offers)
            if "price" in node and not price:
                price = str(node["price"])
            if "availability" in node and not avail:
                avail = str(node["availability"]).rsplit("/", 1)[-1]
            stack.extend(v for v in node.values() if isinstance(v, (dict, list)))
    return price, avail


def scan(ctx, store: str, name: str, url: str) -> Result:
    res = Result(store=store, name=name, url=url)
    page = ctx.new_page()
    try:
        resp = page.goto(url, timeout=60_000, wait_until="domcontentloaded")
        res.status = str(resp.status if resp else "no-response")
        page.wait_for_timeout(3500)  # даём догрузиться цене

        res.jsonld_price, res.jsonld_avail = parse_jsonld(page)

        body = page.inner_text("body")[:200_000]

        # для страниц поиска: вытаскиваем название рядом с ценой,
        # иначе непонятно, к чему относится дешёвый ценник
        for m in PRICE_RE.finditer(body):
            val = (m.group(1) or m.group(2)).replace(",", ".")
            try:
                if float(val) > 130:
                    continue
            except ValueError:
                continue
            ctx = body[max(0, m.start() - 160):m.start()].replace("\n", " | ").strip()
            res.signals.append(f"<=130EUR {val} ← ...{ctx[-140:]}")

        found = []
        for m in PRICE_RE.finditer(body):
            found.append((m.group(1) or m.group(2)).replace(",", "."))
        # уникальные, отсортированные по величине, только правдоподобные
        vals = sorted({float(v) for v in found if 5.0 <= float(v) <= 2000.0})
        res.text_prices = [f"{v:.2f}" for v in vals[:12]]

        if OOS_RE.search(body):
            res.signals.append("OOS-маркер")
        if INSTOCK_RE.search(body):
            res.signals.append("в-наличии-маркер")
    except Exception as exc:  # noqa: BLE001 — хотим увидеть причину в логе
        res.error = f"{type(exc).__name__}: {exc}"[:300]
    finally:
        # своя страница на каждую цель: незавершённая навигация одного сайта
        # больше не срывает переход на следующий
        try:
            page.close()
        except Exception:
            pass
    return res


def main() -> int:
    results: list[Result] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(
            user_agent=UA,
            locale="fr-FR",
            timezone_id="Europe/Paris",
            viewport={"width": 1366, "height": 900},
        )
        for store, name, url in TARGETS:
            print(f"→ {store}: {name}", flush=True)
            results.append(scan(ctx, store, name, url))
        browser.close()

    print("\n" + "=" * 78)
    print("РЕЗУЛЬТАТ СКАНИРОВАНИЯ")
    print("=" * 78)
    for r in results:
        print(f"\n[{r.store}] {r.name}")
        print(f"  HTTP        : {r.status}")
        if r.error:
            print(f"  ОШИБКА      : {r.error}")
            continue
        print(f"  JSON-LD цена: {r.jsonld_price or '—'}")
        print(f"  JSON-LD нал.: {r.jsonld_avail or '—'}")
        print(f"  Цены в тексте: {', '.join(r.text_prices) if r.text_prices else '—'}")
        print(f"  Сигналы     : {', '.join(r.signals) if r.signals else '—'}")

    with open("sup_scan_results.json", "w", encoding="utf-8") as fh:
        json.dump([r.__dict__ for r in results], fh, ensure_ascii=False, indent=2)
    print("\nСохранено в sup_scan_results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
