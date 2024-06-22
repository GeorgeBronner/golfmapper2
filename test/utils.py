from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from main import app
from database import Base
from models import UserCourses, Users
from routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "george", "id": 1, "user_role": "admin"}


client = TestClient(app)

# id = Column(Integer, primary_key=True, index=True)
# course_id = Column(Integer, ForeignKey("courses.id"))
# user_id = Column(Integer, ForeignKey("users.id"))

@pytest.fixture
def test_user_courses():
    user_course = UserCourses(course_id=500, user_id=1)
    db = TestingSessionLocal()
    db.add(user_course)
    db.commit()
    yield user_course
    with engine.connect() as con:
        con.execute(text("DELETE FROM user_courses;"))
        con.commit()

# id = Column(Integer, primary_key=True, index=True)
# email = Column(String, unique=True)
# username = Column(String, unique=True)
# first_name = Column(String)
# last_name = Column(String)
# hashed_password = Column(String)
# is_active = Column(Boolean, default=True)
# role = Column(String)

user = Users(
    email="georgetest@mail.com",
    username="georgetest",
    first_name="firsttest",
    last_name="lasttest",
    hashed_password=bcrypt_context.hash("password"),
    is_active=True,
    role="admin",
)
@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as con:
        con.execute(text("DELETE FROM users;"))
        con.commit()
