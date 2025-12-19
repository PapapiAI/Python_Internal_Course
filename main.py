from fastapi import FastAPI

from controllers.health_controller import health_router
from controllers.user_controller import user_router
from middlewares.db_session import DBSessionMiddleware

app = FastAPI()

# Đăng ký router
app.include_router(health_router, tags=["Health"])
app.include_router(user_router, prefix="/users", tags=["Users"])

app.add_middleware(DBSessionMiddleware) # type: ignore[arg-type]
