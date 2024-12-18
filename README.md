A FastAPI API to manage golf courses played by a user.  Designed to use gm2-react as a frontend.

Currently supports sqlite (default) or postgres as the DB.

Required environmental variables to be set:
SECRET_KEY_AUTH: set to a random string to encode the JWT tokens. 

Optional environmental variables to be set:
DB_USER = postgres user
DB_PASSWORD = postgres password
DB_HOST = postgres host (default localhost)
DB_PORT = postgres port (default 5432)
USE_SQLITE_DB = use qulite over postgres (default true)
SQLITE_DB_URL = SQLITE_DB_URL (default None)
SENTRY_DSN = SENTRY_DSN (default "")
