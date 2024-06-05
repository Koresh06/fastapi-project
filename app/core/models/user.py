from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import Order, Product


class User(Base, IntIdPkMixin):
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255), default="customer") # customer, manager, admin
    is_verified: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # updated_at: Mapped[datetime] = mapped_column(
    #     DateTime(),
    #     default=datetime.utcnow,
    #     onupdate=datetime.utcnow,
    # )

    order_rel: Mapped[List["Order"]] = relationship(back_populates='user_rel', cascade='all, delete')
    product_rel: Mapped[List["Product"]] = relationship(back_populates='user_rel', cascade='all, delete') 