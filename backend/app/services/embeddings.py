"""AWS Bedrock Titan Embeddings Service"""

import json
import os
import boto3
from typing import List


class BedrockEmbeddings:
    """AWS Bedrock Titan Embeddings V2"""

    def __init__(self):
        region = os.getenv("AWS_REGION", "eu-central-1")
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
        self.dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))

    def embed(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(
                {
                    "inputText": text,
                    "dimensions": self.dimensions,
                    "normalize": True,
                }
            ),
        )
        result = json.loads(response["body"].read())
        return result["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts."""
        return [self.embed(t) for t in texts]


_embeddings = None


def get_embeddings() -> BedrockEmbeddings:
    """Get singleton embeddings service."""
    global _embeddings
    if _embeddings is None:
        _embeddings = BedrockEmbeddings()
    return _embeddings
