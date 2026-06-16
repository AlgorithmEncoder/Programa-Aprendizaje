def get_prompt(tema: str, descripcion_tema: str, bloque: dict, temarios: list[dict], tipos_relacion_permitidos: list[str], min_conocimientos: int, max_conocimientos: int) -> str:
    return f"""
Eres un experto en extracción y estructuración de conocimiento para sistemas de aprendizaje.

Tu tarea consiste en analizar los temarios proporcionados y extraer conocimientos educativos explícitos que puedan utilizarse posteriormente para generar preguntas de aprendizaje.

## Objetivo

Extraer conocimientos individuales a partir de los textos proporcionados.

Cada conocimiento debe representar una única idea o afirmación educativa.

Los conocimientos deben estar basados exclusivamente en la información presente en los temarios.

No inventes información.

No añadas conocimientos que no estén respaldados por los textos.

---

## Información disponible

Tema:
{tema}

Descripción del tema:
{descripcion_tema}

Bloque:
{bloque}

Temarios:
{temarios}

Tipos de relación permitidos:
{tipos_relacion_permitidos}

---

## Reglas obligatorias

1. Genera entre {min_conocimientos} y {max_conocimientos} conocimientos.
2. Cada conocimiento debe representar una única relación.
3. No inventes información no presente en los temarios.
4. Usa únicamente tipos de relación permitidos.
5. El campo "relacion" debe ser coherente con "tipo_relacion".
6. Evita duplicados semánticos.
7. Evita conocimientos redundantes.
8. Prioriza relaciones explícitas o directamente inferibles del texto.
9. La explicación debe basarse exclusivamente en los temarios.
10. Evita contradicciones entre conocimientos.
11. Prioriza calidad sobre cantidad.
12. No incluyas texto fuera del JSON.

---

## Ejemplos

### Correcto

Mercurio → es un → planeta

Mercurio → orbita alrededor del → Sol

Sol → está compuesto principalmente por → hidrógeno y helio

---

### Incorrecto

Mercurio → está relacionado con → Sistema Solar

(Relación demasiado ambigua)

---

### Incorrecto

Mercurio → es un planeta que orbita alrededor del → Sol

(Contiene más de una idea)

---

### Incorrecto

Mercurio → pertenece a → Sistema Solar

Si el temario no menciona explícitamente dicha información.

---

## Formato de entrada

Recibirás un objeto JSON con formato:
```json
{
  "bloque": {...},
  "temarios": [...],
  "tipos_relacion_permitidos": [...],
  "max_conocimientos" : 50,
  "min_conocimientos" : 20
}
```

### Ejemplo:
```json
{
  "tema": "Sistema Solar",
  "descripcion_tema": "Aprender la composición, estructura y funcionamiento del Sistema Solar.",
  "tipos_relacion_permitidos": [
		"clasificacion",
		"propiedad",
		"funcion",
		"ubicacion",
		"composicion"
  ],
  "bloque": {
    "numero": 2,
    "titulo": "Planetas interiores",
    "descripcion": "Características y estudio de los planetas más cercanos al Sol."
  },
  "temarios": [
    {
      "titulo": "Mercurio",
      "contenido": "Mercurio es el planeta más cercano al Sol..."
    },
    {
      "titulo": "Venus",
      "contenido": "Venus es el segundo planeta del Sistema Solar..."
    }
  ],
  "max_conocimientos" : 50
  "min_conocimientos" : 20
}
```

---

## Formato de salida

Devuelve únicamente un objeto JSON válido.

La clave principal debe ser:

```json
{
  "conocimientos": []
}

---

### Ejemplo de salida:
```json
{
  "conocimientos": [
    {
      "concepto_a": "Mercurio",
      "tipo_relacion": "clasificacion",
      "relacion": "es un",
      "concepto_b": "planeta",
      "explicacion": "Mercurio pertenece a la categoría de los planetas del Sistema Solar."
    },
    {
      "concepto_a": "Mercurio",
      "tipo_relacion": "ubicacion",
      "relacion": "orbita alrededor del",
      "concepto_b": "Sol",
      "explicacion": "Mercurio gira alrededor del Sol siguiendo una órbita estable."
    }
  ]
}
```
"""