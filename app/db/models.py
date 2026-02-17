from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, JSON
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    source: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(Text)
    headers: Mapped[dict] = mapped_column(JSON)
    query_params: Mapped[dict] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

