from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPUTH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
