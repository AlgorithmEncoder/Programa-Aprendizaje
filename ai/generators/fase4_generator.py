from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase4_conocimientos import get_prompt


class Fase4Generator(BaseGenerator):

    def generate(
        self,
        tema: str,
        descripcion_tema: str,
        bloque: dict,
        temarios: list[dict],
        tipos_relacion_permitidos: list[str],
        min_conocimientos: int,
        max_conocimientos: int
    ):

        prompt = get_prompt(
            tema=tema,
            descripcion_tema=descripcion_tema,
            bloque=bloque,
            temarios=temarios,
            tipos_relacion_permitidos=tipos_relacion_permitidos,
            min_conocimientos=min_conocimientos,
            max_conocimientos=max_conocimientos
        )

        return self.run_json(prompt)