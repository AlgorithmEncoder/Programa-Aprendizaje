from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase3_temario import get_prompt


class Fase3Generator(BaseGenerator):

    def generate(
        self,
        tema: str,
        descripcion_tema: str,
        bloque: dict,
        fragmentos_deseados: int,
        min_palabras_fragmento: int = 300,
        max_palabras_fragmento: int = 700
    ):

        prompt = get_prompt(
            tema=tema,
            descripcion_tema=descripcion_tema,
            bloque=bloque,
            fragmentos_deseados=fragmentos_deseados,
            min_palabras_fragmento=min_palabras_fragmento,
            max_palabras_fragmento=max_palabras_fragmento
        )

        return self.run_json(prompt)