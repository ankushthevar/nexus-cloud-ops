from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import (
    create_incident,
    get_incident,
    get_incidents,
)


router = APIRouter()


@router.post(
    "/incidents",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident_endpoint(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
):
    return create_incident(
        db=db,
        incident_data=incident_data,
    )


@router.get(
    "/incidents",
    response_model=list[IncidentResponse],
)
def list_incidents(
   skip: int = Query(0, ge=0),
   limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_incidents(
        db=db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse,
)
def retrieve_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = get_incident(
        db=db,
        incident_id=incident_id,
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident