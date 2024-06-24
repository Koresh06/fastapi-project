from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.product.service import ProductService
from core.models.product import Product
from core.models import db_helper


async def product_by_uid(
    product_uid: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Product:
    product = await ProductService(session).get_product(product_uid)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_uid} not found!",
    )