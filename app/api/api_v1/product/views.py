import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validator import get_current_active_auth_user
from api.api_v1.user.schemas import UserSchema
from api.api_v1.product.service import ProductService
from core.models import db_helper

from .schemas import ProductCreationModel, ProductBase


router = APIRouter(
    tags=["products"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
async def create_product(
    product: ProductCreationModel = Depends(ProductCreationModel.as_form),
    user: UserSchema = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    if product.image_url:
        UPLOAD_DIRECTORY = "D:\\Python\\fastapi-project\\app\\api\\images"
        file_path = os.path.join(UPLOAD_DIRECTORY, product.image_url.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(product.image_url.file, buffer)
    
    result = await ProductService(session=session).create_new_product(
        data=product, user=user, image_url=product.image_url.filename if product.image_url else None
    )
    
    return result
    
    