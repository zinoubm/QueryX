import qdrant_client
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]


class VectorClient:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(
            host=os.environ["QDRANT_DB_HOST"],
            port=os.environ["QDRANT_DB_PORT"],
            api_key=os.environ["QDRANT_API_KEY"],
        )

    def embed(self, prompt, model="text-similarity-ada-001"):
        prompt = prompt.replace("\n", " ")
        embedding = None
        try:
            embedding = openai.Embedding.create(input=[prompt], model=model)["data"][0][
                "embedding"
            ]
        except Exception as err:
            print(f"Sorry, There was a problem {err}")

        return embedding

    def search(self, query_embedding):
        query_results = self.client.search(
            collection_name="upsto_test",
            query_vector=query_embedding,
            limit=50,
        )
        return query_results

    def chat_completrion(self, prompt):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion

    def answer(self, query):
        query_embedding = self.embed(prompt=query)

        query_results = self.client.search(
            collection_name="twitter_tos",
            query_vector=query_embedding,
            limit=4,
        )

        contexts = [query_result.payload["content"] for query_result in query_results]

        joined_context = "\n".join(contexts)

        prompt = f"""
        
        Question Prompt: Given the context below, answer the following question using only 
        the provided information and without referring to prior knowledge:

        Context:

        "{joined_context}"

        Question: {query}
        
        """

        test = self.chat_completrion(prompt=prompt)

        return test["choices"][0]["message"]["content"]
