from fastapi import Depends, APIRouter, Request, Path, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from database import get_async_session
from models import Follow
from schemas.base import Success
from schemas.user import GetUser

router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@router.get(
    "/api/users/{id}",
    tags=["User"],
    response_model=GetUser,
)
async def get_user_id(
        id: int | str = Path(
            ...,
            title="Item ID",
            description="You can use int or if you want get yours data use `me`",
            example="me",
        ),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Get user data and his followers and following.
    """

    if id == "me":
        id = fastapi_users.current_user
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")

    user_exist = await User.get_user(id=id, session=session)

    follower = await Follow.get_follower(id=id, session=session)
    following = await Follow.get_following(id=id, session=session)
    if user_exist:
        response = {"result": True, "user": user_exist}
        response["user"].update({"followers": follower})
        response["user"].update({"following": following})
        return JSONResponse(response, status_code=200)

    raise HTTPException(status_code=400, detail="User dont exist.")


@router.post(
    "/api/users/{id}/follow",
    tags=["User"],
    response_model=Success,
)
async def post(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Subscribe to user by id.
    """
    self_user = fastapi_users.current_user()
    if not self_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await Follow.handler_follower(
        from_user_id=self_user,
        to_user_id=id,
        method="POST",
        session=session,
    )
    if result:
        data = {"result": True}
        return JSONResponse(data, status_code=201)
    raise HTTPException(status_code=400, detail="User dont exist.")


@router.delete(
    "/api/users/{id}/follow",
    tags=["User"],
    response_model=Success,
)
async def delete(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Unsubscribe from user by id.
    """
    self_user = fastapi_users.current_user.id
    if not self_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await Follow.handler_follower(
        from_user_id=self_user,
        to_user_id=id,
        method="DELETE",
        session=session,
    )
    if result:
        data = {"result": True}
        return JSONResponse(data, status_code=204)
    raise HTTPException(status_code=400, detail="User dont exist.")
