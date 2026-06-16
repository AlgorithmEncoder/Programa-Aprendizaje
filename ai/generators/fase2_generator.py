from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase2_agrupacion import get_prompt


class Fase2Generator(BaseGenerator):

    def generate(self, conceptos: list[dict], numero_bloques: int):

        prompt = get_prompt(
            conceptos=conceptos,
            numero_bloques=numero_bloques
        )

        return self.run_json(prompt)