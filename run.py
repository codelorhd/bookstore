from datetime import datetime
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY

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

app = FastAPI(
    title="Bookstore API Documentation",
    description="This is a bookstore api",
    version="1.0.0",
)
# adding dependencies of check_jwt_token will add authorization check in all endpoints
app.include_router(
    app_v1,
    prefix="/v1",
    dependencies=[Depends(check_jwt_token)],
)
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.middleware("http")
async def middleware(request: Request, call_next):
    """
    Allows only authenticated request.
    The middleware also adds execution time to the header for all endpoints.
    """
    start_time = datetime.utcnow()
    # modify the request: excempt the token endpoint
    if not any(
        word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]
    ):
        try:
            # headers may not include Authorization key
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False

        if not is_valid:
            return Response("Unauthorized", status.HTTP_401_UNAUTHORIZED)

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
    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # create jwt for the user
    jwt_token = create_jwt_token(user=user)

    # access_token can not be changed
    return {"access_token": jwt_token}
