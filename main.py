import fastapi
from routers import users
from db.db_setup import setup
app = fastapi.FastAPI()
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    await setup()
