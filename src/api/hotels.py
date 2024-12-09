from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependecies import PaginationDep
from src.database import async_session_maker
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
    hotel_id: int | None = Query(None, description="Номер отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if hotel_id:
            query = query.filter_by(id=hotel_id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels

    # return hotels_[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай у моря",
                    "location": "ул. Шейха, 2",
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
