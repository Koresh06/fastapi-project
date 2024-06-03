from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Float, Integer

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import Product, Order


class OrderItems(Base, IntIdPkMixin):
    order_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey("product.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    
    order_rel: Mapped["Order"] = relationship(back_populates="items_rel")
    product_rel: Mapped["Product"] = relationship(back_populates="items_rel")