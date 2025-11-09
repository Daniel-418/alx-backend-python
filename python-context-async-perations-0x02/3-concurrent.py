import sqlite3
import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("select * from user_data") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("select * from user_data where age > ?", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(), async_fetch_older_users()
    )
    print("fetches complete.")
    print(f"All users: {all_users}")
    print(f"Older users: {older_users}")


asyncio.run(fetch_concurrently())

