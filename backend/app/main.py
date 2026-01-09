from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.auth import get_current_user, require_admin
from app.config import settings
from app.database import Base, engine, get_session
from app.models import User
from app.redis_client import redis_client
from app.schemas import TokenResponse, UserCreate, UserLogin, UserPublic, UserStatusUpdate
from app.security import create_access_token

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.admin_email and settings.admin_password:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.email == settings.admin_email))
            existing = result.scalar_one_or_none()
            if existing is None:
                await crud.create_user(
                    session=session,
                    email=settings.admin_email,
                    password=settings.admin_password,
                    is_admin=True,
                )


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await redis_client.aclose()


@app.post(f"{settings.api_prefix}/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"register:{client_ip}"
    attempts = await redis_client.incr(rate_key)
    if attempts == 1:
        await redis_client.expire(rate_key, 3600)
    if attempts > 5:
        raise HTTPException(status_code=429, detail="注册过于频繁，请稍后再试")

    existing = await crud.get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已注册")
    user = await crud.create_user(session, payload.email, payload.password)
    return UserPublic.model_validate(user)


@app.post(f"{settings.api_prefix}/login", response_model=TokenResponse)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    user = await crud.authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    access_token = create_access_token(subject=user.email)
    return TokenResponse(access_token=access_token)


@app.get(f"{settings.api_prefix}/me", response_model=UserPublic)
async def get_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)


@app.get(f"{settings.api_prefix}/admin/users", response_model=list[UserPublic])
async def admin_list_users(
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> list[UserPublic]:
    users = await crud.list_users(session)
    return [UserPublic.model_validate(user) for user in users]


@app.patch(f"{settings.api_prefix}/admin/users/{user_id}", response_model=UserPublic)
async def admin_update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = payload.is_active
    await session.commit()
    await session.refresh(user)
    return UserPublic.model_validate(user)
