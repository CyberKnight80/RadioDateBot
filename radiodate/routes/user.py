from http.client import HTTPException

from fastapi import APIRouter, HTTPException, Depends, Body

from radiodate.db.connection import Transaction
from radiodate.models.like import Like
from radiodate.models.user import User
from radiodate.schemas.user import UserView, UserUpdateView

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{telegram_id}")
async def profile(telegram_id: int):
    async with Transaction():
        user: UserView = await User.get_by_telegram_id(telegram_id=telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/{telegram_id}", status_code=200)
async def profile(telegram_id: int, body: UserUpdateView = Body(...)):

    async with Transaction():
        user: UserView = await User.get_by_telegram_id(telegram_id=telegram_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await User.update(user_id=user.id, body=body)
    return


# SWIPES
@router.get("/{telegram_id}/next", status_code=200)
async def next_profile(telegram_id: int):

    async with Transaction():
        user: UserView = await User.get_by_telegram_id(telegram_id=telegram_id)

        matches = await Like.get_match(user_id=user.id)

        if matches:
            love = await User.get(value=matches)
            await Like.delete_match(user_id=user.id, matched_user_id=love.id)
            return {"status": "match", "user": UserView.model_validate(love.as_dict())}

        victim = await User.get_random_user()
        while victim.telegram_id == user.telegram_id:
            victim = await User.get_random_user()

        return victim
