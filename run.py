from datetime import datetime
from utils.const import REDIS_URL, TOKEN_DESCRIPTION, TOKEN_SUMMARY

from fastapi.exceptions import HTTPException
from models.jwt_user import JWTUser
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from utils.security import authenticate_user, check_jwt_token, create_jwt_token
from fastapi import FastAPI
from routes.v1 import app_v1
from routes.v2 import app_v2

from starlette.requests import Request
from starlette.responses import Response
from starlette import status

from utils.db_object import db
import utils.redis_object as re
import aioredis

app = FastAPI(
    title="Bookstore API Documentation",
    description="This is a bookstore api",
    version="1.0.0",
)

# adding dependencies of check_jwt_token will add authorization check in all endpoints
# You can add multiple dependencies
app.include_router(
    app_v1,
    prefix="/v1",
    dependencies=[Depends(check_jwt_token), Depends(re.check_test_redis)],
)
app.include_router(
    app_v2,
    prefix="/v2",
    dependencies=[Depends(check_jwt_token), Depends(re.check_test_redis)],
)

# --------------- DATABASE AND REDIS CONNECTION AND DISCONNECTION ---------------

# Note these events will not be in called when testing.

@app.on_event("startup")
async def connect_db():
    await db.connect()
    re.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")
async def discconnect_db():
    await db.disconnect()
    re.redis.close()

    await re.redis.wait_closed()


# --------------- DATABASE AND REDIS  CONNECTION AND DISCONNECTION ---------------


@app.middleware("http")
async def middleware(request: Request, call_next):
    """
    Allows only authenticated request.
    The middleware also adds execution time to the header for all endpoints.
    """
    start_time = datetime.utcnow()

    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["X-Execution-Time"] = str(execution_time)
    return response


# exempt this endpoint from authorization check
@app.post(
    "/token",
    description=TOKEN_DESCRIPTION,
    summary=TOKEN_SUMMARY,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}

    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # create jwt for the user
    jwt_token = create_jwt_token(user=user)

    # access_token can not be changed
    return {"access_token": jwt_token}
