def get_prompt(tema: str, descripcion_tema: str, bloque: dict, preguntas: list[dict], respuestas_incorrectas_por_pregunta: int, dificultad_distractores: str) -> str:
    return f"""
Eres un experto en diseño de evaluaciones educativas y creación de preguntas tipo test.

Tu tarea consiste en generar respuestas incorrectas plausibles para cada pregunta proporcionada.

Estas respuestas formarán parte de preguntas de selección múltiple.

## Objetivo

Generar exactamente {respuestas_incorrectas_por_pregunta} respuestas incorrectas para cada pregunta.

Las respuestas incorrectas deben ser plausibles, coherentes con el contexto y claramente incorrectas.

## Información de entrada

Tema:
{tema}

Descripción:
{descripcion_tema}

Bloque:
{bloque}

Preguntas:
{preguntas}

Nivel de dificultad de distractores:
{dificultad_distractores}

## Reglas obligatorias

1. Genera exactamente {respuestas_incorrectas_por_pregunta} distractores por pregunta.
2. Los distractores deben pertenecer al mismo dominio semántico.
3. No deben ser absurdos ni humorísticos.
4. No deben ser parcialmente correctos.
5. No deben contener la respuesta correcta.
6. No deben repetirse dentro de la misma pregunta.
7. Mantén coherencia con el nivel de dificultad:
   - baja: relacionados pero claramente incorrectos
   - media: plausibles dentro del mismo contexto
   - alta: altamente confundibles
8. Evita patrones evidentes de exclusión.
9. Mantén coherencia dentro del bloque.
10. No incluyas texto fuera del JSON.

## Formato de salida

{
  "preguntas": [
    {
      "pregunta": "...",
      "respuesta_correcta": "...",
      "respuestas_incorrectas": [
        "...",
        "...",
        "..."
      ]
    }
  ]
}

---

## Ejemplos

### Ejemplo 1

Pregunta:

¿Qué planeta es el más cercano al Sol?

Respuesta correcta: Mercurio

Respuestas incorrectas válidas:

- Venus
- Tierra
- Marte

---

### Ejemplo 2

Pregunta:

¿De qué está compuesto principalmente el Sol?

Respuesta correcta: Hidrógeno y helio

Respuestas incorrectas válidas:

- Oxígeno y nitrógeno
- Hierro y níquel
- Carbono y silicio

---

### Ejemplo incorrecto

Pregunta:

¿Qué planeta es el más cercano al Sol?

Respuesta correcta: Mercurio

Respuestas incorrectas:

- Bicicleta
- Montaña
- Perro

Las respuestas no pertenecen al mismo contexto conceptual.

---

## Formato de entrada

Recibirás un objeto JSON con formato:

```json
{
  "tema": "...",
  "descripcion_tema": "...",
  "bloque": {...},
  "preguntas": [...],
  "respuestas_incorrectas_por_pregunta": 3,
  "dificultad_distractores": "alta/media/baja"
}
```

### Ejemplo

```json
{
  "tema": "Sistema Solar",
  "descripcion_tema": "Aprender la composición, estructura y funcionamiento del Sistema Solar.",
  "bloque": {
    "numero": 2,
    "titulo": "Planetas interiores",
    "descripcion": "Características y estudio de los planetas más cercanos al Sol."
  },
  "preguntas": [
    {
      "pregunta": "¿Qué tipo de cuerpo celeste es Mercurio?",
      "respuesta_correcta": "Planeta"
    },
    {
      "pregunta": "¿Alrededor de qué astro orbita Mercurio?",
      "respuesta_correcta": "El Sol"
    }
  ],
  "respuestas_incorrectas_por_pregunta": 3,
  "dificultad_distractores": "alta"
  }
```

---

## Formato de salida

Devuelve únicamente un objeto JSON válido.

La clave principal debe ser:

```json
{
  "preguntas": []
}
```

Cada elemento debe tener exactamente esta estructura:

```json
{
  "pregunta": "Texto de la pregunta",
  "respuesta_correcta": "Texto de la respuesta correcta",
  "respuestas_incorrectas": [
    "Respuesta incorrecta 1",
    "Respuesta incorrecta 2",
    "Respuesta incorrecta 3"
  ]
}
```

---

## Ejemplo de salida

```json
{
  "preguntas": [
    {
      "pregunta": "¿Qué tipo de cuerpo celeste es Mercurio?",
      "respuesta_correcta": "Planeta",
      "respuestas_incorrectas": [
        "Satélite natural",
        "Cometa",
        "Asteroide"
      ]
    },
    {
      "pregunta": "¿Alrededor de qué astro orbita Mercurio?",
      "respuesta_correcta": "El Sol",
      "respuestas_incorrectas": [
        "La Tierra",
        "Júpiter",
        "Saturno"
      ]
    }
  ]
}
```

---

## Validaciones que debes respetar

- Todas las preguntas deben aparecer en la salida.
- Ninguna pregunta puede omitirse.
- Cada pregunta debe tener exactamente {respuestas_incorrectas_por_pregunta} respuestas incorrectas.
- La respuesta correcta no puede aparecer entre las incorrectas.
- No puede haber respuestas duplicadas.
- Todas las respuestas incorrectas deben ser claramente incorrectas.
- Todas las respuestas incorrectas deben ser plausibles.

---

## Resultado esperado

Devuelve únicamente JSON válido siguiendo exactamente la estructura solicitada.
"""