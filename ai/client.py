import json

from openai import OpenAI

from config.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE_DEFAULT,
    COST_PER_1K_INPUT_TOKENS,
    COST_PER_1K_OUTPUT_TOKENS
)


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def generate_json(
        self,
        prompt,
        model=OPENAI_MODEL,
        temperature=TEMPERATURE_DEFAULT
    ):

        response = self.client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature
        )

        content = response.output_text

        usage = self._extract_usage(response)

        return {
            "content": self._safe_json_parse(content),
            "tokens_input": usage["tokens_input"],
            "tokens_output": usage["tokens_output"],
            "cost_estimated": usage["cost_estimated"],
            "model": model
        }

    def generate_text(
        self,
        prompt,
        model=OPENAI_MODEL,
        temperature=TEMPERATURE_DEFAULT
    ):

        response = self.client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature
        )

        usage = self._extract_usage(response)

        return {
            "content": response.output_text,
            "tokens_input": usage["tokens_input"],
            "tokens_output": usage["tokens_output"],
            "cost_estimated": usage["cost_estimated"],
            "model": model
        }

    def _extract_usage(self, response):

        input_tokens = getattr(
            response.usage,
            "input_tokens",
            0
        )

        output_tokens = getattr(
            response.usage,
            "output_tokens",
            0
        )

        cost = (
            (input_tokens / 1000)
            * COST_PER_1K_INPUT_TOKENS
        ) + (
            (output_tokens / 1000)
            * COST_PER_1K_OUTPUT_TOKENS
        )

        return {
            "tokens_input": input_tokens,
            "tokens_output": output_tokens,
            "cost_estimated": round(cost, 6)
        }

    def _safe_json_parse(self, content):

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"La IA no devolvió JSON válido: {exc}"
            )