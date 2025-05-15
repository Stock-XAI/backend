# tests/conftest.py
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.session import Base

@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},  # sqlite 스레드 허용
        echo=False,
    )
    Base.metadata.create_all(engine)          # 테이블 생성
    Session = sessionmaker(bind=engine)

    with Session() as session:
        yield session                         # 여기서 테스트 실행
        # 자동 rollback·close
    # with 블록을 벗어나면 engine 도 GC 되면서 메모리 DB 제거
