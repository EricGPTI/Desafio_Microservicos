from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    notification: str