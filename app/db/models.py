from datetime import datetime, timezone

from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    severity: Mapped[IncidentSeverity] = mapped_column(
    SQLEnum(
        IncidentSeverity,
        values_callable=lambda enum: [item.value for item in enum],
    ),
    nullable=False,
    default=IncidentSeverity.MEDIUM,
)

    status: Mapped[IncidentStatus] = mapped_column(
    SQLEnum(
        IncidentStatus,
        values_callable=lambda enum: [item.value for item in enum],
    ),
    nullable=False,
    default=IncidentStatus.OPEN,
)

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    service: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )