from pydantic import BaseModel

class CategoriaRequest(BaseModel):
    categoria: str