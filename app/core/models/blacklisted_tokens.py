from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime

from core.models.base import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class BlacklistedToken(Base, IntIdPkMixin):

    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    blacklisted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)