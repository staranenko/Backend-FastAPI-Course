from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependecies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title}%').collate("ru_RU.UTF-8"))
        if location:
            query = query.filter(HotelsOrm.location.like(f'%{location}%').collate("ru_RU.UTF-8"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)

        return result.scalars().all()


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"success": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        hotel["title"] = hotel_data.title
        hotel["name"] = hotel_data.name
    return {"success": "OK"}


@router.patch("/{hotel_id}")
def partial_edit_hotel(hotel_id: int, hotel_data: HotelPUTH):
    global hotels
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if hotel_data.title and hotel["title"] != hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.name and hotel["name"] != hotel_data.name:
            hotel["name"] = hotel_data.name
    return {"success": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    print(hotels)
    return {"status": "OK"}
