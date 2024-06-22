from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import engine
from routers import garmin_courses, garmin_courses_no_auth, auth, admin, users, user_courses, user_courses_no_auth
from models import Base


app = FastAPI()
Base.metadata.create_all(bind=engine)

origins = [
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/healthy", status_code=200)(lambda: {"message": "I'm healthy"})
app.include_router(auth.router)
app.include_router(garmin_courses.router)
app.include_router(garmin_courses_no_auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(user_courses.router)
app.include_router(user_courses_no_auth.router)
