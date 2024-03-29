from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

import random
import string


def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(4))
    return random_string


async def test_user_model(db: AsyncSession):
    user = User(
        id=uuid4().hex,
        email=generate_random_string() + "@exampsadfle.com",
        hashed_password="12sdf34",
    )
    db.add(user)
    await db.commit()
    assert user.id
