from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField
from torque.models import SearchCacheDocument


class SemanticSearchCacheDocument(models.Model):
    search_cache_document = models.ForeignKey(
        SearchCacheDocument,
        on_delete=models.CASCADE,
        related_name="semantic_documents",
    )
    data = models.TextField()
    data_embedding = VectorField(
        dimensions=getattr(settings, "SEMANTIC_SEARCH_NUM_DIMENSIONS", 768),
        null=True,
    )

    class Meta:
        indexes = [
            HnswIndex(
                name="data_embedding_index",
                fields=["data_embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            ),
        ]
