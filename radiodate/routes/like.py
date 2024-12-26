from fastapi import APIRouter, HTTPException

from radiodate.db.connection import Transaction
from radiodate.models.like import Like
from radiodate.models.user import User

router = APIRouter(prefix="/likes")


@router.get("/{telegram_id}/{other_telegram_id}", tags=["like"])
async def like_victim(telegram_id: int, other_telegram_id: int):

    async with Transaction():

        liker = await User.get_by_telegram_id(telegram_id=telegram_id)

        if not liker:
            return HTTPException(
                status_code=404, detail=f"User with telegram id {telegram_id} not found"
            )

        liked = await User.get_by_telegram_id(telegram_id=other_telegram_id)
        if not liked:
            return HTTPException(
                status_code=404, detail=f"User with telegram id {telegram_id} not found"
            )
        await Like.like(liker.id, liked.id)
