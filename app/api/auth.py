from fastapi import APIRouter, HTTPException, status
from talkingdb.clients.sqlite import sqlite_conn
from talkingdb.helpers.auth import hash_password, verify_password
from talkingdb.helpers.jwt import create_access_token
from talkingdb.models.auth.auth import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from talkingdb.models.auth.user import UserModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(payload: SignupRequest):
    try:
        with sqlite_conn() as conn:
            UserModel.create(
                conn=conn,
                email=payload.email,
                password_hash=hash_password(
                    payload.password
                ),
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    return SignupResponse(
        message="Account created successfully"
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(payload: LoginRequest):
    with sqlite_conn() as conn:
        user = UserModel.find_by_email(
            conn,
            payload.email,
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        {"sub": user.email}
    )

    return LoginResponse(
        access_token= token,
        message= "Successfully logined"
    )