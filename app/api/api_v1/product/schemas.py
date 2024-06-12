import uuid
from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    
    uid: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: str
    price: float
    image_url: Optional[UploadFile | str]

class ProductCreationModel(ProductBase):

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        image_url: UploadFile = File(None),
    ):
        return cls(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
        )