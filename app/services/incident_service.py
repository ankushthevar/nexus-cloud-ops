from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Incident, IncidentStatus
from app.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    incident_data: IncidentCreate,
) -> Incident:
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        status=IncidentStatus.OPEN,
        source=incident_data.source,
        service=incident_data.service,
        detected_at=incident_data.detected_at,
    )

    try:
        db.add(incident)
        db.commit()
        db.refresh(incident)
    except Exception:
        db.rollback()
        raise

    return incident


def get_incidents(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Incident]:
    statement = (
        select(Incident)
        .order_by(Incident.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def get_incident(
    db: Session,
    incident_id: int,
) -> Incident | None:
    return db.get(Incident, incident_id)