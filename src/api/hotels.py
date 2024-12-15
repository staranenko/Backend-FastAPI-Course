from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependecies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPUTH

router = APIRouter(prefix="/hotels", tags=["Hotels"])


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


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
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
        hotel_data: Hotel = Body(
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
def partial_edit_hotel(hotel_id: int, hotel_data: HotelPUTH):
    global hotels
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if hotel_data.title and hotel["title"] != hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.location and hotel["name"] != hotel_data.location:
            hotel["name"] = hotel_data.location
    return {"success": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
