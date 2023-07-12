from httpx import AsyncClient

from app.core.config import settings
from app.models.user import User
from tests.utils import get_jwt_header


class TestQuery:
    async def test_query(
        self,
        client: AsyncClient,
        create_user,
    ):
        user: User = await create_user()
        jwt_header = get_jwt_header(user)
        payload = {"query": "What is the meaning of life?", "filename": "example.txt"}
        resp = await client.post(
            settings.API_PATH + "/queries/",
            json=payload,
            headers=jwt_header,
        )
        assert resp.status_code == 200
