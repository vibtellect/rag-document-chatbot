"""AWS Bedrock Claude LLM Service"""

import json
import os
import boto3


class BedrockLLM:
    """AWS Bedrock Claude service wrapper."""

    def __init__(self):
        region = os.getenv("AWS_REGION", "eu-central-1")
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
        self.default_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2048"))
        self.default_temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    def generate(
        self,
        user_prompt: str,
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate text with Claude."""

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens or self.default_max_tokens,
            "temperature": temperature if temperature is not None else self.default_temperature,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        if system_prompt:
            body["system"] = system_prompt

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]


_llm = None


def get_llm() -> BedrockLLM:
    """Get singleton LLM service."""
    global _llm
    if _llm is None:
        _llm = BedrockLLM()
    return _llm
