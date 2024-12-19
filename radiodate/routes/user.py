from fastapi import APIRouter

from radiodate.db.connection import Transaction
from radiodate.models.user import User

router = APIRouter(prefix="/user")


@router.get("/next/")
async def get_next_user():

    async with Transaction():
        user = await User.get_random_user()
    return user
