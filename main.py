import fastapi
from routers import users
app = fastapi.FastAPI()
app.include_router(users.router)
