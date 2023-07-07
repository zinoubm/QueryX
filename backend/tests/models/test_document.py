from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.user import User

import random
import string


def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(4))
    return random_string


def generate_random_3digit_int():
    return int(random.randint(100, 999))


async def test_document_model(db: AsyncSession):
    user_id = uuid4()
    user = User(
        id=user_id,
        email=generate_random_string() + "@exampsadfle.com",
        hashed_password="12sdf34",
    )
    document = Document(
        id=generate_random_3digit_int(), user_id=user_id, name="Impact_of_tech.pdf"
    )
    db.add(user)
    db.add(document)
    await db.commit()
    assert document.id
