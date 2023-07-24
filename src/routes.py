from fastapi import APIRouter
from src.user.routers import auth_router, user_router
from src.task.router import task_router


routes = APIRouter()

routes.include_router(auth_router)

routes.include_router(
    task_router,
    prefix="/task",
    tags=["task"],
)

routes.include_router(
    user_router,
    prefix="/user",
    tags=["user"],
)




