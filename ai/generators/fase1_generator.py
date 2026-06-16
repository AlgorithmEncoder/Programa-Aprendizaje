from ai.generators.base_generator import BaseGenerator
from ai.prompts.fase1_esquematizacion import get_prompt


class Fase1Generator(BaseGenerator):

    def generate(self, tema: str, descripcion: str | None = None):

        prompt = get_prompt(
            tema=tema,
            descripcion=descripcion
        )

        return self.run_json(prompt)