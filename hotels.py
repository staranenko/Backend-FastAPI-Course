from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@router.get("", summary="Получить все отели", description="Нужно указать или номер или название или и то и другое. Для получения всех отелей параметры не заполнять.")
def get_hotels(
    hotel_id: int | None = Query(None, description="Номер отеля"),
    title: str | None = Query(None,
                              description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("")
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
            "name": name,
        }
    )
    return {"success": "OK"}


@router.put("/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        hotel["title"] = title
        hotel["name"] = name
    return {"success": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            hotel["title"] = title
        if name and hotel["name"] != name:
            hotel["name"] = name
    return {"success": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    print(hotels)
    return {"status": "OK"}