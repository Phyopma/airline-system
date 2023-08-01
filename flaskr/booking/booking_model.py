from datetime import datetime
from pydantic import BaseModel


class Booking(BaseModel):
    passenger_id: int
    flight_id: int
    seat_id: int
    booking_at: datetime = datetime.now()
