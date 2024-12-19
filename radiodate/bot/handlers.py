from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command

from radiodate.db.connection import Transaction
from radiodate.models.user import User
from radiodate.settings import get_settings

bot = Bot(token=get_settings().TELEGRAM_API_TOKEN)


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    # message.from_user.id
    async with Transaction():
        user = await User.get_by_telegram_id(message.from_user.id)

        if not user:
            await User.create(telegram_id=message.from_user.id)
