from typing import Any, List, Dict

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User, Follow


async def get_user(id: int = 1, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    data = await session.execute(select(User).where(User.id == id))
    result = {}
    if data:
        result['id'] = data.id
        result['name'] = data.name
    return result


async def get_follower(
        id=1,
        session: AsyncSession = Depends(get_db)
) -> List[Dict]:
    data = await session.execute(select(Follow).where(Follow.to_user_id == id))
    result = []
    if data:
        result = [
            {'id': x.from_user.id, 'name': x.from_user.name}
            for x in data
        ]
    return result


async def get_following(
        id=1,
        session: AsyncSession = Depends(get_db)
) -> List[Dict]:
    data = await session.execute(select(Follow).where(Follow.from_user_id == id))
    result = []
    if data:
        result = [
            {'id': x.to_user.id, 'name': x.to_user.name}
            for x in data
        ]
    return result
