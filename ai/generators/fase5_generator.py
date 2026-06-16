from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase5_preguntas import get_prompt


class Fase5Generator(BaseGenerator):

    def generate(
        self,
        tema: str,
        descripcion_tema: str,
        bloque: dict,
        conocimientos: list[dict],
        min_preguntas: int,
        max_preguntas: int
    ):

        prompt = get_prompt(
            tema=tema,
            descripcion_tema=descripcion_tema,
            bloque=bloque,
            conocimientos=conocimientos,
            min_preguntas=min_preguntas,
            max_preguntas=max_preguntas
        )

        return self.run_json(prompt)