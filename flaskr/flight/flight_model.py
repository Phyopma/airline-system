from datetime import datetime

from pydantic import BaseModel, PositiveInt


class Flight(BaseModel):
    airline_id: int
    origin_city_id: int
    destination_city_id: int
    total_seats: int
    departure_time: datetime = datetime.now()
    duration: str
    price: int
