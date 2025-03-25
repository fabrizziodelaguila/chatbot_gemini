from pydantic import BaseModel

class Destino(BaseModel):
    name: str
    description: str
    price: float
    rating: float
