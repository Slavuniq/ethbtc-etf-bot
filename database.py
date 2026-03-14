import aiosqlite
import time

from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                person_photo TEXT,
                tries_left INTEGER DEFAULT 5,
                total_generations INTEGER DEFAULT 0,
                referrer_id INTEGER,
                created_at REAL,
                last_active REAL
            )"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS generations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                garment_photo TEXT,
                result_photo TEXT,
                quality_score REAL,
                created_at REAL
            )"""
        )
        await db.commit()


async def get_user(uid):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        c = await db.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        r = await c.fetchone()
        return dict(r) if r else None


async def create_user(uid, uname, fname, tries, ref=None):
    n = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(user_id,username,full_name,tries_left,referrer_id,created_at,last_active) VALUES(?,?,?,?,?,?,?)",
            (uid, uname, fname, tries, ref, n, n),
        )
        await db.commit()


async def update_person_photo(uid, path):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET person_photo=?,last_active=? WHERE user_id=?",
            (path, time.time(), uid),
        )
        await db.commit()


async def use_try(uid):
    async with aiosqlite.connect(DB_PATH) as db:
        c = await db.execute("SELECT tries_left FROM users WHERE user_id=?", (uid,))
        r = await c.fetchone()
        if not r or r[0] <= 0:
            return False
        await db.execute(
            "UPDATE users SET tries_left=tries_left-1,total_generations=total_generations+1,last_active=? WHERE user_id=?",
            (time.time(), uid),
        )
        await db.commit()
        return True


async def add_tries(uid, n):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET tries_left=tries_left+? WHERE user_id=?", (n, uid)
        )
        await db.commit()


async def save_generation(uid, cat, gp, rp, q):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO generations(user_id,category,garment_photo,result_photo,quality_score,created_at) VALUES(?,?,?,?,?,?)",
            (uid, cat, gp, rp, q, time.time()),
        )
        await db.commit()


async def get_user_generations(uid, limit=6):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        c = await db.execute(
            "SELECT * FROM generations WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
            (uid, limit),
        )
        return [dict(r) for r in await c.fetchall()]


async def get_stats():
    async with aiosqlite.connect(DB_PATH) as db:
        tu = (await (await db.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        tg = (await (await db.execute("SELECT COUNT(*) FROM generations")).fetchone())[0]
        at = (
            await (
                await db.execute(
                    "SELECT COUNT(*) FROM users WHERE last_active>?",
                    (time.time() - 86400,),
                )
            ).fetchone()
        )[0]
        return {"total_users": tu, "total_generations": tg, "active_today": at}


async def get_referral_count(uid):
    async with aiosqlite.connect(DB_PATH) as db:
        return (
            await (
                await db.execute(
                    "SELECT COUNT(*) FROM users WHERE referrer_id=?", (uid,)
                )
            ).fetchone()
        )[0]
