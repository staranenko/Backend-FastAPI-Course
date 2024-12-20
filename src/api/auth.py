from fastapi import APIRouter, HTTPException, status

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UsersAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UsersAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user_exists = await UsersRepository(session).get_one_or_none(email=new_user_data.email)
        if user_exists is not None:
            # Возврат HTTP 409 с понятным описанием
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким адресом электронной почты уже существует"
            )

        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK", "message": "Пользователь успешно зарегистрирован"}
