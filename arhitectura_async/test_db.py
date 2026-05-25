import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        user="postgres",
        password="2762",
        database="vscode",
        host="127.0.0.1"
    )
    print("CONNECTED")
    await conn.close()

asyncio.run(test())