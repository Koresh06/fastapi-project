from typing import Optional
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.user.schemas import UserSchema

from core.models.product import Product
from api.api_v1.product.schemas import ProductCreationModel, ProductUpdateModel


class ProductService:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def delete_product(self, product: Product):
        await self.session.delete(product)
        await self.session.commit()


    async def update_product(
            self, 
            product: Product,
            product_update: ProductUpdateModel,
            partil: bool = False
            ) -> Product:
        for field, value in product_update.model_dump(exclude_unset=partil).items():
            setattr(product, field, value)
        await self.session.commit()
        return product


    async def get_product(self, uid: str) -> Product | None:
        stmt: Result = await self.session.scalar(select(Product).where(Product.uid == uid))
        return stmt


    async def get_all_products(self, limit: int, offset: int) -> list[Product] | None:
        statement = select(Product).limit(limit).offset(offset)
        stmt: Result = await self.session.scalars(statement)
        return stmt


    async def create_new_product(self, data: ProductCreationModel, user: UserSchema, image_url: Optional[str]) -> Product:
        product = Product(
            user_id=user.uid,
            name=data.name,
            description=data.description,
            price=data.price,
            image_url=image_url,
        )
        self.session.add(product)
        await self.session.commit()
        return product