"""
Стартовый сборщик лидов через ОФИЦИАЛЬНЫЙ Instagram Graph API.

Что умеет (легально, без скрейпа):
  1) Hashtag Search  — найти свежие/топ публичные посты по хэштегу.
  2) Business Discovery — по @username публичного бизнес/креатор-аккаунта вернуть
     bio, число подписчиков, кол-во постов, недавние медиа.

Чего НЕ умеет (ограничения Meta, а не скрипта):
  - нет поиска по локации и по ключевым словам;
  - не отдаёт имена лайкеров/комментаторов (нет PII);
  - hashtag search: максимум 30 уникальных хэштегов за 7 дней, 200 запросов/час.

Требуется (это даёт владелец проекта):
  - IG Business/Creator аккаунт, связанный с Facebook Page;
  - долгоживущий access token с правами:
    instagram_basic, instagram_manage_insights, pages_show_list,
    business_management, + Instagram Public Content Access (для hashtag search).

Запуск:
  export IG_TOKEN="EAAB..."          # access token
  export IG_USER_ID="178414..."      # ID твоего IG бизнес-аккаунта
  python scripts/ig_graph_collect.py
"""

import csv
import os
import sys
import time

import requests  # pip install requests

GRAPH = "https://graph.facebook.com/v21.0"

# Хэштеги, отсекающие именно US-кластер про Ривьеру (пересечение гео x "американский").
HASHTAGS = [
    "americaninfrance", "americaninnice", "expatinfrance", "frenchriviera",
    "cotedazur", "southoffrance", "frenchrivieratravel", "cotedazurtravel",
]

# Эталонные публичные бизнес/креатор-аккаунты для Business Discovery (из seed-листа).
SEED_USERNAMES = [
    "heleneinbetween", "theamericaninparis", "nicefrance_life",
    "experiencethefrenchriviera",
]


def _get(path, params):
    params = {**params, "access_token": TOKEN}
    r = requests.get(f"{GRAPH}/{path}", params=params, timeout=30)
    if r.status_code != 200:
        print(f"  ! API {r.status_code}: {r.text[:200]}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def hashtag_recent(tag, limit=50):
    """Свежие публичные посты по одному хэштегу."""
    hid = _get("ig_hashtag_search", {"user_id": IG_USER_ID, "q": tag}).get("data", [])
    if not hid:
        return []
    hid = hid[0]["id"]
    fields = "id,caption,permalink,like_count,comments_count,timestamp"
    res = _get(f"{hid}/recent_media",
               {"user_id": IG_USER_ID, "fields": fields, "limit": limit})
    rows = []
    for m in res.get("data", []):
        rows.append({
            "source": f"#{tag}",
            "permalink": m.get("permalink", ""),
            "likes": m.get("like_count", 0),
            "comments": m.get("comments_count", 0),
            "timestamp": m.get("timestamp", ""),
            "caption": (m.get("caption", "") or "").replace("\n", " ")[:200],
        })
    return rows


def business_profile(username):
    """Публичный профиль бизнес/креатор-аккаунта по @username."""
    fields = (f"business_discovery.username({username})"
              "{username,name,biography,followers_count,media_count,website}")
    bd = _get(IG_USER_ID, {"fields": fields}).get("business_discovery", {})
    if not bd:
        return None
    return {
        "username": bd.get("username", username),
        "name": bd.get("name", ""),
        "followers": bd.get("followers_count", 0),
        "media": bd.get("media_count", 0),
        "website": bd.get("website", ""),
        "bio": (bd.get("biography", "") or "").replace("\n", " ")[:200],
    }


def main():
    posts, profiles = [], []

    print("== Hashtag search ==")
    for tag in HASHTAGS:
        try:
            rows = hashtag_recent(tag)
            posts += rows
            print(f"  #{tag}: {len(rows)} постов")
            time.sleep(1)  # бережём rate limit (200/час)
        except Exception as e:  # noqa: BLE001
            print(f"  #{tag}: пропуск ({e})")

    print("== Business discovery ==")
    for u in SEED_USERNAMES:
        try:
            p = business_profile(u)
            if p:
                profiles.append(p)
                print(f"  @{u}: {p['followers']} подписчиков")
            time.sleep(1)
        except Exception as e:  # noqa: BLE001
            print(f"  @{u}: пропуск ({e})")

    if posts:
        with open("riviera_posts.csv", "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=posts[0].keys()).writeheader()
            csv.DictWriter(f, fieldnames=posts[0].keys()).writerows(posts)
        print(f"-> riviera_posts.csv ({len(posts)} строк)")
    if profiles:
        with open("riviera_profiles.csv", "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=profiles[0].keys()).writeheader()
            csv.DictWriter(f, fieldnames=profiles[0].keys()).writerows(profiles)
        print(f"-> riviera_profiles.csv ({len(profiles)} строк)")


if __name__ == "__main__":
    TOKEN = os.getenv("IG_TOKEN")
    IG_USER_ID = os.getenv("IG_USER_ID")
    if not TOKEN or not IG_USER_ID:
        sys.exit("Задай переменные окружения IG_TOKEN и IG_USER_ID (см. docstring).")
    main()
