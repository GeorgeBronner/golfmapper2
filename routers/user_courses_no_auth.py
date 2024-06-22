from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from models import Courses, UserCourses
from routers.auth import get_current_user, get_test_user
from sqlalchemy import func
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import geopy.geocoders
import certifi
import ssl
from typing import Optional


ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx   #reenable

router = APIRouter(prefix="/user_courses_no_auth", tags=["user_courses_no_auth"])

@router.get("/")
async def root():
    return {"message": "Hello World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_test_user)]

class UserCourseRequest(BaseModel):
    garmin_id: int = Field(...)


@router.get("/readall_ids", status_code=status.HTTP_200_OK)
async def readall_ids(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(UserCourses).filter(UserCourses.user_id == user.get("id")).all()


@router.get("/readall", status_code=status.HTTP_200_OK)
async def readall(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")


    # Query the database to fetch all course IDs associated with the user
    course_ids = (
        db.query(UserCourses.course_id)
        .filter(UserCourses.user_id == user.get("id"))
        .distinct()  # Select distinct course IDs
        .all()
    )

    # Extract course IDs from the query result
    course_ids = [course_id for course_id, in course_ids]

    # Query the database to fetch all courses with the retrieved course IDs
    courses = (
        db.query(Courses)
        .filter(Courses.id.in_(course_ids))  # Filter courses by the retrieved IDs
        .all()
    )

    return courses


@router.post("/add_course", status_code=status.HTTP_201_CREATED)
async def add_user_course(user: user_dependency, db: db_dependency, user_course_request: UserCourseRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_course_model = UserCourses(course_id=user_course_request.garmin_id, user_id=user.get("id"))
    db.add(user_course_model)
    db.commit()
#

@router.delete("/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_course(user: user_dependency, db: db_dependency, course_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_course_model = db.query(UserCourses).filter(UserCourses.course_id == course_id).filter(UserCourses.user_id == user.get("id")).first()
    if user_course_model is None:
        raise HTTPException(status_code=404, detail="Course_id not found")
    db.delete(user_course_model)
    db.commit()
