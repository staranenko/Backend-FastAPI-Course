from fastapi import Query, APIRouter, Body


from src.api.dependecies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPUTH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить все отели",
    description="Нужно указать или номер или название или и то и другое. Для получения всех отелей параметры не заполнять.",
)
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get(
    "/{hotel_id}",
    summary="Получить отель по идентификатору",
)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Благоухание лотоса",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Luxury rest by sea",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Благоухание лотоса",
                        "location": "Сочи, ул. Моря, 1",
                    },
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Luxury rest by sea",
                        "location": "Дубай, ул. Шейха, 2",
                    },
                },
            }
        ),
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"success": "OK"}


@router.patch("/{hotel_id}")
async def partial_edit_hotel(hotel_id: int, hotel_data: HotelPUTH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"success": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
