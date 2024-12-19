from fastapi import APIRouter


router = APIRouter(prefix="/user")


@router.get("/")
async def home_window():
    pass
