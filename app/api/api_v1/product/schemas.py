import uuid
from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class ProductBase(BaseModel):
    
    uid: uuid.UUID
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
            uid=uuid.uuid4(),
            name=name,
            description=description,
            price=price,
            image_url=image_url,
        )

class ProductUpdateModel(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    # image_url: Optional[UploadFile | str] = None