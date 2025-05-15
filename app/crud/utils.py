# app/crud/utils.py
from contextlib import contextmanager
from typing import Optional
from sqlalchemy.orm import Session
from db.session import SessionLocal

@contextmanager
def get_session(ext_session: Optional[Session] = None):
    if ext_session:
        yield ext_session
    else:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()
