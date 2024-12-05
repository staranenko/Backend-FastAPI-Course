from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPUTH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary="Получить все отели", description="Нужно указать или номер или название или и то и другое. Для получения всех отелей параметры не заполнять.")
def get_hotels(
    hotel_id: int | None = Query(None, description="Номер отеля"),
    title: str | None = Query(None, description="Название отеля"),
    page: int | None = Query(1, ge=1, description="Номер страницы"),
    per_page: int | None = Query(10, ge=1, description="Количество отелей на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    start = page * per_page - per_page
    end = start + per_page
    return hotels_[start:end]


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи у моря",
        "name": "sochi_by_sea",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у моря",
        "name": "dubai_by_sea",
    }},
})
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
        }
    )
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
def partial_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPUTH
):
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