from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import Order, Product


class User(Base, IntIdPkMixin):
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255), default="customer") # roles: admin, manager, customer

    order_rel: Mapped[List["Order"]] = relationship(back_populates='user_rel', cascade='all, delete')
    product_rel: Mapped[List["Product"]] = relationship(back_populates='product_rel', cascade='all, delete')