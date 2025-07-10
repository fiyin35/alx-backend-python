import aiosqlite
import asyncio

DB_NAME = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        print("All Users:")
        for row in rows:
            print(row)
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        print("\nUsers older than 40:")
        for row in rows:
            print(row)
        return rows

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the async function
asyncio.run(fetch_concurrently())
