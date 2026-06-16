def get_prompt(tema:str, descripcion_tema:str, json_bloque: dict, min_temarios: int, max_temarios: int, min_palabras_fragmento: int = 300, max_palabras_fragmento: int = 700):
    return f"""
Eres un experto en diseño curricular, redacción de material educativo y creación de contenido para sistemas de aprendizaje.

Tu tarea consiste en generar temario educativo para un bloque de aprendizaje.

El temario será utilizado posteriormente para extraer conocimientos, generar preguntas y construir actividades educativas.

## Objetivo

Generar contenido didáctico que permita aprender los conceptos asignados al bloque de forma progresiva, clara y rigurosa.

El contenido debe estar orientado al aprendizaje y contener información suficiente para comprender correctamente los conceptos tratados.

---

## Información disponible

Tema:

{tema}

Descripción del tema:

{descripcion_tema}

Bloque:

{json_bloque}

Número de fragmentos deseados:

De {min_temarios} a a{max_temarios}

Número de plabras por fragmento:

De {min_palabras_fragmento} a {max_palabras_fragmento}

---

## Reglas obligatorias

1. Redacta texto expositivo continuo.
2. Cada fragmento debe ser una unidad de aprendizaje independiente.
3. Cada fragmento debe poder entenderse sin leer los anteriores.
4. Todos los conceptos del bloque deben ser explicados en conjunto.
5. No introduzcas contenido ajeno al bloque.
6. Ordena los fragmentos de menor a mayor complejidad.
7. Cada fragmento debe centrarse en uno o pocos conceptos estrechamente relacionados.
8. El contenido debe ser expositivo y claro.
9. No incluyas ejercicios, preguntas, conclusiones o resúmenes.
10. No utilices listas ni esquemas.
11. No añadas texto fuera del JSON.

---

## Recomendaciones pedagógicas

1. Introduce primero los conceptos más generales.

2. Explica posteriormente los conceptos más específicos.

3. Cuando existan relaciones entre conceptos, descríbelas explícitamente dentro del texto.

4. Siempre que sea posible, explica:
   - qué es algo;
   - para qué sirve;
   - de qué está compuesto;
   - cómo se relaciona con otros conceptos;
   - cuáles son sus características principales.

5. Prioriza la claridad frente a la complejidad técnica.

6. Ordena los fragmentos desde lo más introductorio a lo más complejo dentro del bloque.

---

## Formato de salida

Devuelve únicamente un objeto JSON válido.

La clave principal debe ser:

```json
{
  "temarios": []
}
```

Cada fragmento debe tener exactamente la siguiente estructura:

```json
{
  "titulo": "Título del fragmento",
  "contenido": "Texto educativo del fragmento"
}
```

---

## Ejemplo de formato esperado

```json
{
  "temarios": [
    {
      "titulo": "Introducción a los planetas interiores",
      "contenido": "Los planetas interiores son los planetas más cercanos al Sol..."
    },
    {
      "titulo": "Mercurio",
      "contenido": "Mercurio es el planeta más próximo al Sol..."
    }
  ]
}
```

---

## Resultado esperado

Devuelve únicamente JSON válido siguiendo exactamente la estructura solicitada.
"""