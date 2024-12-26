import asyncio

import uvicorn
from aiogram import Dispatcher, Bot
from fastapi import FastAPI

from radiodate.routes import user_router

from radiodate.bot.handlers import router as bot_router
from radiodate.settings import get_settings

app = FastAPI()

app.include_router(user_router)

bot = Bot(token=get_settings().TELEGRAM_API_TOKEN)
dp = Dispatcher()

dp.include_routers(bot_router)


async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
