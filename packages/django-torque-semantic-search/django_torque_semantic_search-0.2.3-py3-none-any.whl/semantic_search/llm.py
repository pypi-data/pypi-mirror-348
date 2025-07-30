import requests
from django.conf import settings
from sentence_transformers import SentenceTransformer


class LLM:
    def __init__(self):
        self.api_base = getattr(settings, "SEMANTIC_SEARCH_EMBEDDING_API_BASE_URL")
        self.api_key = getattr(settings, "SEMANTIC_SEARCH_EMBEDDING_API_KEY")
        self.model_name = getattr(settings, "SEMANTIC_SEARCH_EMBEDDING_MODEL")
        self.session = requests.Session()

    def get_embeddings(self, texts, *, prompt_name=None) -> list[list[float]]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"input": texts, "model": self.model_name}
        if prompt_name:
            data["type"] = prompt_name

        num_retries = 0
        while num_retries < 5:
            response = self.session.post(
                f"{self.api_base}/embeddings", json=data, headers=headers
            )
            if response.status_code == 200:
                break
            num_retries = num_retries + 1

        if num_retries == 5:
            raise Exception("get_embeddings call failed too many times")

        payload = response.json()
        results = payload.get("data", [])
        embeddings = [result.get("embedding") for result in results]

        return embeddings


class LocalLLM(LLM):
    def __init__(self):
        self.model_name = getattr(settings, "SEMANTIC_SEARCH_EMBEDDING_MODEL")
        self.model = SentenceTransformer(
            self.model_name,
            trust_remote_code=True,
            config_kwargs={"use_memory_efficient_attention": False},
        )

    def get_embeddings(self, texts, *, prompt_name=None):
        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(texts, prompt_name=prompt_name).tolist()


llm = LLM()
local_llm = LocalLLM()
