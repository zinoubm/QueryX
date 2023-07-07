from app.core.config import settings

# from app.vectorstore.qdrant import VectorClient
from app.vectorstore.qdrant import QdrantManager


import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def test_get_collection_info():
    manager = QdrantManager()
    collection_info = manager.get_collection_info()
    assert collection_info is not None


def test_upsert_point():
    manager = QdrantManager()
    record_id = uuid4().hex
    record_payload = {"title": "Dreaming big", "chunk": "wow this is great"}
    record_embedding = get_embedding(record_payload["chunk"])

    response = manager.upsert_point(record_id, record_payload, record_embedding)
    assert response is not None


def test_upsert_batch():
    manager = QdrantManager()
    record_ids = [uuid4().hex for x in range(3)]
    record_payloads = [
        {
            "title": "War",
            "chunk": """
                War is an intense armed conflict[a] between states, governments, societies, or paramilitary groups such as mercenaries, insurgents, and militias. It is generally characterized by extreme violence, destruction, and mortality, using regular or irregular military forces. Warfare refers to the common activities and characteristics of types of war, or of wars in general.[2] Total war is warfare that is not restricted to purely legitimate military targets, and can result in massive civilian or other non-combatant suffering and casualties.
                While some war studies scholars consider war a universal and ancestral aspect of human nature,[3] others argue it is a result of specific socio-cultural, economic or ecological circumstances.[4]
            """,
        },
        {
            "title": "Car",
            "chunk": """
                A car or automobile is a motor vehicle with wheels. Most definitions of cars say that they run primarily on roads, seat one to eight people, have four wheels, and mainly transport people (rather than goods).
            """,
        },
        {
            "title": "Horse",
            "chunk": "The horse (Equus ferus caballus)[2][3] is a domesticated, one-toed, hoofed mammal. It belongs to the taxonomic family Equidae and is one of two extant subspecies of Equus ferus. The horse has evolved over the past 45 to 55 million years from a small multi-toed creature, Eohippus, into the large, single-toed animal of today. Humans began domesticating horses around 4000 BCE, and their domestication is believed to have been widespread by 3000 BCE. Horses in the subspecies caballus are domesticated, although some domesticated populations live in the wild as feral horses. These feral populations are not true wild horses, as this term is used to describe horses that have never been domesticated. There is an extensive, specialized vocabulary used to describe equine-related concepts, covering everything from anatomy to life stages, size, colors, markings, breeds, locomotion, and behavior.",
        },
    ]
    record_embeddings = get_embeddings(
        [record_payload["chunk"] for record_payload in record_payloads]
    )

    response = manager.upsert_points(record_ids, record_payloads, record_embeddings)
    assert response is not None


def test_search_point():
    manager = QdrantManager()
    query_embedding = get_embedding("what are my rights?")

    response = manager.search_point(query_embedding, 1)
    assert response is not None


def test_delete_collection():
    manager = QdrantManager()
    response = manager.delete_collection()
    assert response is not None


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY

# manager = QdrantManager()

# collection_info = manager.get_collection_info()
# print(collection_info)

# # upsert a point
# record_id = uuid4().hex
# record_payload = {"title": "Dreaming big", "chunk": "wow this is great"}
# record_embedding = get_embedding(record_payload["chunk"])

# response = manager.upsert_point(
#     record_id,
#     record_payload,
#     record_embedding,
# )

# # upsert batch
# record_ids = [uuid4().hex for x in range(3)]
# record_payloads = [
#     {
#         "title": "War",
#         "chunk": """
#             War is an intense armed conflict[a] between states, governments, societies, or paramilitary groups such as mercenaries, insurgents, and militias. It is generally characterized by extreme violence, destruction, and mortality, using regular or irregular military forces. Warfare refers to the common activities and characteristics of types of war, or of wars in general.[2] Total war is warfare that is not restricted to purely legitimate military targets, and can result in massive civilian or other non-combatant suffering and casualties.
#             While some war studies scholars consider war a universal and ancestral aspect of human nature,[3] others argue it is a result of specific socio-cultural, economic or ecological circumstances.[4]
#         """,
#     },
#     {
#         "title": "Car",
#         "chunk": """
#             A car or automobile is a motor vehicle with wheels. Most definitions of cars say that they run primarily on roads, seat one to eight people, have four wheels, and mainly transport people (rather than goods).
#      """,
#     },
#     {
#         "title": "Horse",
#         "chunk": "The horse (Equus ferus caballus)[2][3] is a domesticated, one-toed, hoofed mammal. It belongs to the taxonomic family Equidae and is one of two extant subspecies of Equus ferus. The horse has evolved over the past 45 to 55 million years from a small multi-toed creature, Eohippus, into the large, single-toed animal of today. Humans began domesticating horses around 4000 BCE, and their domestication is believed to have been widespread by 3000 BCE. Horses in the subspecies caballus are domesticated, although some domesticated populations live in the wild as feral horses. These feral populations are not true wild horses, as this term is used to describe horses that have never been domesticated. There is an extensive, specialized vocabulary used to describe equine-related concepts, covering everything from anatomy to life stages, size, colors, markings, breeds, locomotion, and behavior.",
#     },
# ]
# record_embeddings = get_embeddings(
#     [record_payload["chunk"] for record_payload in record_payloads]
# )

# response = manager.upsert_points(
#     record_ids,
#     record_payloads,
#     record_embeddings,
# )

# # getting collection_info
# collection_info = manager.get_collection_info()
# print(collection_info)

# # search point
# query_embedding = get_embedding("what are my rights?")

# response = manager.search_point(query_embedding, 1)

# print(response)

# # delete all points
# res = manager.delete_collection()
# print(res)
