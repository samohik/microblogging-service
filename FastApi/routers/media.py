from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

router = APIRouter()


@router.post("/api/medias")
async def post_media(session: AsyncSession = Depends(get_async_session)):
    """
    POST /api/medias
    HTTP-Params:
    api-key: str
    form: file=”image.jpg”
    В ответ должен вернуться id загруженного файла.
    {
        “result”: true,
        “media_id”: int
    }
    """
    # todo post add_media
    response = {"result": True, "tweet_id": 1}
    return response, 201
