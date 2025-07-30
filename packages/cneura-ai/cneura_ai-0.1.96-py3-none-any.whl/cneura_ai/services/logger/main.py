import asyncio
import websockets
import json
from datetime import datetime
import aiofiles
import asyncpg
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

WEBSOCKET_SERVER = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8765))

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
}

LOG_FILE = "logs/server.log"
os.makedirs("logs", exist_ok=True)


async def save_to_file(log_data: str):
    async with aiofiles.open(LOG_FILE, mode='a') as f:
        await f.write(log_data + '\n')

async def save_to_db(pool, json_data: dict):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO logs (timestamp, service, level, message)
            VALUES ($1, $2, $3, $4)
        ''',
            json_data.get('timestamp'),
            json_data.get('service'),
            json_data.get('level'),
            json_data.get('message')
        )


async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                timestamp TEXT,
                service TEXT,
                level TEXT,
                message TEXT
            )
        ''')

async def log_handler(websocket, pool):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                data['timestamp'] = datetime.now().isoformat()

                await save_to_file(json.dumps(data))
                await save_to_db(pool, data)

                logger.info(f"✅ \t- {data.get('service')} - {data.get('message')}")
            except Exception as e:
                logger.error(f"❌ \tError handling message: {e}")
    except websockets.ConnectionClosed:
        logger.warning("❌ \tClient disconnected.")

async def main():
    pool = await asyncpg.create_pool(**DB_CONFIG)
    await init_db(pool)
    async with websockets.serve(lambda ws: log_handler(ws, pool), WEBSOCKET_SERVER, WEBSOCKET_PORT):
        print(f"🟢 \tLogging server started at ws://{WEBSOCKET_SERVER}:{WEBSOCKET_PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
