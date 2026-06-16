from ai.client import OpenAIClient
from utils.logger import get_logger


class BaseGenerator:

    def __init__(self):
        self.client = OpenAIClient()
        self.logger = get_logger(self.__class__.__name__)

    def run_json(self, prompt: str):
        """
        Ejecuta prompt contra OpenAI y devuelve respuesta estructurada.
        """

        self.logger.info("Ejecutando generación IA")

        result = self.client.generate_json(prompt)

        self.logger.info(
            "Generación completada | tokens_in=%s tokens_out=%s cost=%s",
            result["tokens_input"],
            result["tokens_output"],
            result["cost_estimated"]
        )

        return result

    def run_text(self, prompt: str):
        """
        Si alguna fase necesita texto plano.
        """

        self.logger.info("Ejecutando generación IA (texto)")

        result = self.client.generate_text(prompt)

        return result