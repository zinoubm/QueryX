import qdrant_client


def get_qdrant_client():
    return qdrant_client.QdrantClient(host=host, port=port, api_key=qdrant_api_key)
