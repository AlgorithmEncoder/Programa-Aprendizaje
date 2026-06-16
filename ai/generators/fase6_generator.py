from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase6_respuestas_incorrectas import get_prompt


class Fase6Generator(BaseGenerator):

    def generate(
        self,
        tema: str,
        descripcion_tema: str,
        bloque: dict,
        preguntas: list[dict],
        respuestas_incorrectas_por_pregunta: int,
        dificultad_distractores: str
    ):

        prompt = get_prompt(
            tema=tema,
            descripcion_tema=descripcion_tema,
            bloque=bloque,
            preguntas=preguntas,
            respuestas_incorrectas_por_pregunta=respuestas_incorrectas_por_pregunta,
            dificultad_distractores=dificultad_distractores
        )

        return self.run_json(prompt)