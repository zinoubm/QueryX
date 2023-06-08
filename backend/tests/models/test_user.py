from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def test_user_model(db: AsyncSession):
    user = User(id=uuid4(), email="tessdft@exampsadfle.com", hashed_password="12sdf34")
    db.add(user)
    await db.commit()
    assert user.id
