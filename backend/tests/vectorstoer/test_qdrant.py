from app.core.config import settings
from app.vectorstore.qdrant import VectorClient


async def test_answer():
    client = VectorClient()
    answer = client.answer("What is twitter?")
    assert answer
