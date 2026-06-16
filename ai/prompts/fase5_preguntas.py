def get_prompt(tema:str, descripcion_tema:str, bloque: dict, conocimientos: list[dict], min_preguntas: int, max_preguntas: int) -> str:
    return f"""
Eres un experto en diseño de evaluaciones educativas y creación de preguntas para sistemas de aprendizaje.

Tu tarea consiste en generar preguntas de evaluación a partir de una lista de conocimientos estructurados.

Cada pregunta debe servir para comprobar si el estudiante ha adquirido correctamente un conocimiento específico.

---

## Objetivo

Generar preguntas claras, directas y no ambiguas que evalúen conocimientos individuales.

Cada pregunta debe basarse exclusivamente en la información proporcionada.

---

## Reglas obligatorias

1. Cada pregunta debe evaluar únicamente un conocimiento.
2. Cada conocimiento debe estar representado al menos una vez.
3. No combines varios conocimientos en una misma pregunta.
4. No inventes información.
5. Evita preguntas ambiguas o con múltiples respuestas posibles.
6. Evita preguntas cuya respuesta esté explícita en la pregunta.
7. La respuesta debe ser breve y consistente (preferentemente término o frase nominal).
8. Cada pregunta debe incluir referencia al conocimiento de origen.
9. No incluyas texto fuera del JSON.
10. Genera entre {min_preguntas} y {max_preguntas} preguntas.

---

## Recomendaciones de diseño

- Prioriza preguntas directas de comprensión.
- Varía la estructura de las preguntas (qué es, cómo, dónde, cuál es la función, etc.).
- Asegúrate de que cada pregunta tenga una única respuesta correcta clara.
- Evita preguntas demasiado obvias o triviales.
- Evita preguntas demasiado complejas o indirectas.

---

## Información de entrada

Tema:
{tema}

Descripción:
{descripcion_tema}

Bloque:
{bloque}

Conocimientos:
{conocimientos}

---

## Formato de salida

Devuelve únicamente un objeto JSON válido.

La clave principal debe ser:

```json
{
  "preguntas": []
}
```

---

## Estructura de cada pregunta

Cada elemento del array debe tener exactamente esta estructura:

```json
{
  "pregunta": "Texto de la pregunta",
  "respuesta_correcta": "Texto de la respuesta"
}
```

---

## Ejemplos

### Correcto

```json
{
  "pregunta": "¿Qué tipo de cuerpo celeste es Mercurio?",
  "respuesta_correcta": "Planeta"
}
```

```json
{
  "pregunta": "¿Alrededor de qué astro orbita Mercurio?",
  "respuesta_correcta": "El Sol"
}
```

---

### Incorrecto

```text
¿Qué planeta es Mercurio?
```

(La respuesta está implícita en la pregunta)

---

### Incorrecto

```text
Mercurio es un planeta que orbita alrededor de...
```

(Contiene múltiples ideas)

---

## Resultado esperado

Devuelve únicamente JSON válido siguiendo exactamente la estructura solicitada.
"""