from __future__ import annotations

from sqlalchemy.orm import Session

from athena.models.api import Response


def get_response(session: Session, response_id: int) -> Response | None:
    return session.query(Response).filter(Response.id == response_id).first()


def create_response(session: Session, response: Response) -> Response:
    session.add(response)
    session.commit()
    session.refresh(response)
    return response
