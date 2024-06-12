from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import User, OrderItems


class Product(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.uid"))
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    user_rel: Mapped["User"] = relationship(back_populates='product_rel')
    items_rel: Mapped[List["OrderItems"]] = relationship(back_populates='product_rel', cascade='all, delete')
