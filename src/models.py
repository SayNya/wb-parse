from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    text: str
    rating: int = Field(ge=1, le=5)


class ProductModel(BaseModel):
    id: int
    name: str
    rating: float = Field(ge=1, le=5)
