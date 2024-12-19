from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UsersAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = ""
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}