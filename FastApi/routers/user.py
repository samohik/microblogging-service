from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from main import router
from models import User, Follow


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

    user_exist = User.get_user(id)

    follower = Follow.get_follower(id)
    following = Follow.get_following(id)

    if user_exist:
        response = {
            "result": True,
            "user": user_exist
        }
        response["user"].update({"followers": follower})
        response["user"].update({"following": following})
    else:
        response = {
            "result": False,
            #     "error_type": e,
            #     "error_message": e.messages,
        }
        return response, 400
    return response, 200

@router.get('/api/users/me')
async def get_user_me(
        session: AsyncSession = Depends(get_async_session)
):
    """
    GET /api/users/me
    HTTP-Params:
    api-key: str
    """
    self_id = 1
    data = User.get_user(self_id)

    follower = Follow.get_follower(self_id)
    following = Follow.get_following(self_id)

    response = {
        "result": True,
        "user": data
    }
    response["user"].update({"followers": follower})
    response["user"].update({"following": following})
    return response, 200

def post(
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
    result = Follow.handler_follower(
        from_user_id=1,
        to_user_id=id,
        method="POST"
    )
    response = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }
    if result:
        response = {"result": True}
    return response, 201

def delete(
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
    result = Follow.handler_follower(
        from_user_id=1,
        to_user_id=id,
        method="DELETE",
    )
    response = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }
    if result:
        response = {"result": True}
    return response, 204