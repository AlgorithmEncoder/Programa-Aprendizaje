from pathlib import Path

ROOT = Path.cwd()

folders = [
    "config",
    "database",
    "database/repositories",
    "ai",
    "ai/prompts",
    "ai/generators",
    "validators",
    "services",
    "models",
    "logs"
]

files = [
    "main.py",

    "config/settings.py",

    "database/db.py",
    "database/db_setup.py",

    "database/repositories/temas_repository.py",
    "database/repositories/bloques_repository.py",
    "database/repositories/temarios_repository.py",
    "database/repositories/conocimientos_repository.py",
    "database/repositories/preguntas_repository.py",
    "database/repositories/generaciones_repository.py",

    "ai/client.py",

    "ai/prompts/fase1_esquematizacion.py",
    "ai/prompts/fase2_agrupacion.py",
    "ai/prompts/fase3_temario.py",
    "ai/prompts/fase4_conocimientos.py",
    "ai/prompts/fase5_preguntas.py",
    "ai/prompts/fase6_respuestas_incorrectas.py",

    "ai/generators/fase1_generator.py",
    "ai/generators/fase2_generator.py",
    "ai/generators/fase3_generator.py",
    "ai/generators/fase4_generator.py",
    "ai/generators/fase5_generator.py",
    "ai/generators/fase6_generator.py",

    "validators/fase1_validator.py",
    "validators/fase2_validator.py",
    "validators/fase3_validator.py",
    "validators/fase4_validator.py",
    "validators/fase5_validator.py",
    "validators/fase6_validator.py",

    "services/generation_service.py",
    "services/tema_service.py",
    "services/recovery_service.py",

    "models/tema.py",
    "models/bloque.py",
    "models/temario.py",
    "models/conocimiento.py",
    "models/pregunta.py",

    "README.md",
    "ESTRUCTURA_PROYECTO.md"
]


def create_structure():
    for folder in folders:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)

    for file in files:
        path = ROOT / file

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

    print("Estructura creada correctamente.")


if __name__ == "__main__":
    create_structure()