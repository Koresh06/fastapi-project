import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user.schemas import UserSchema
from api.api_v1.product.service import ProductService
from api.api_v1.product.dependencies import product_by_uid
from api.api_v1.auth.dependencies import RolesChecker, get_current_user
from core.models import db_helper
from .schemas import ProductCreationModel, ProductBase, ProductUpdateModel


router = APIRouter(
    tags=["products"],
)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: ProductBase = Depends(product_by_uid),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin", "manager"])),
):
    await ProductService(session).delete_product(product=product)

    return JSONResponse(
        content={
            "message": f"Delete product - {product.name}"
        },
        status_code=status.HTTP_200_OK
    )



@router.patch("/update", status_code=status.HTTP_200_OK, response_model=ProductBase)
async def update_product(
    product_update: ProductUpdateModel,
    product: ProductBase = Depends(product_by_uid),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin", "manager"])),
):
    return await ProductService(session).update_product(
        product=product,
        product_update=product_update,
        partil=True,
    )


@router.get("/get", status_code=status.HTTP_200_OK, response_model=ProductBase)
async def get_product(
    product: ProductBase = Depends(product_by_uid),
    _: bool = Depends(RolesChecker(["admin", "manager", "customer"])),
):
    return product


@router.get("/get_all", status_code=status.HTTP_200_OK, response_model=List[ProductBase])
async def get_all_products(
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin", "manager", "customer"])),
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
):
    products = await ProductService(session).get_all_products(limit=limit, offset=offset)
    return products


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
async def create_product(
    product: ProductCreationModel = Depends(ProductCreationModel.as_form),
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserSchema = Depends(get_current_user),
    _: bool = Depends(RolesChecker(["admin", "manager"])),
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
    
    
