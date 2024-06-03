from typing import List, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Float

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from models import  User, OrderItems


class Order(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    status: Mapped[str] = mapped_column(String(255), default="pending")# statuses: pending, completed, canceled
    total_price: Mapped[float] = mapped_column(Float)
    
    user_rel: Mapped["User"] = relationship(back_populates='order_rel')
    items_rel: Mapped[List["OrderItems"]] = relationship(back_populates='order_rel')