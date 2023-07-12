from fastapi import Depends, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from database import get_async_session
from models import User, Follow


router = APIRouter()


@router.get('/api/users/{id}')
async def get_user_id(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    GET /api/users/<id>
    Пользователь может получить информацию о произвольном
     профиле по его id:
    """
    user_exist = await User.get_user(
        id=id,
        session=session
    )

    follower = await Follow.get_follower(
        id=id,
        session=session
    )
    following = await Follow.get_following(
        id=id,
        session=session
    )
    response = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }

    if user_exist:
        response = {
            "result": True,
            "user": user_exist
        }
        response["user"].update({"followers": follower})
        response["user"].update({"following": following})
        return JSONResponse(response, status_code=200)

    return JSONResponse(response, status_code=400)


@router.get('/api/users/me')
async def get_user_me(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    GET /api/users/me
    HTTP-Params:
    api-key: str
    """

    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    data = await User.get_user(
        id=self_id,
        session=session,
    )

    follower = await Follow.get_follower(
        id=self_id,
        session=session,
    )
    following = await Follow.get_following(
        id=self_id,
        session=session
    )

    response = {
        "result": True,
        "user": data
    }
    response["user"].update({"followers": follower})
    response["user"].update({"following": following})
    return JSONResponse(response, status_code=200)


@router.post('/api/users/{id}/follow')
async def post(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    POST /api/users/<id>/follow
    HTTP-Params:
    api-key: str
    В ответ должно вернуться сообщение о статусе операции.
    {
        “result”: true
    }
    """
    result = await Follow.handler_follower(
        from_user_id=1,
        to_user_id=id,
        method="POST",
        session=session,
    )
    data = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }
    if result:
        data = {"result": True}
    return JSONResponse(data, status_code=201)


@router.delete('/api/users/{id}/follow')
async def delete(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """DELETE /api/users/<id>/follow
    HTTP-Params:
    api-key: str
    В ответ должно вернуться сообщение о статусе операции.
    {
        “result”: true
    }
    """
    result = await Follow.handler_follower(
        from_user_id=1,
        to_user_id=id,
        method="DELETE",
        session=session,
    )
    data = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }
    if result:
        data = {"result": True}
    return JSONResponse(data, status_code=204)
