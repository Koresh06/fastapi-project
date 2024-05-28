from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import User, OrderItems


class Product(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str] = mapped_column(String)

    user_rel: Mapped["User"] = relationship(back_populates='product_rel')
    items_rel: Mapped[List["OrderItems"]] = relationship(back_populates='product_rel', cascade='all, delete')
