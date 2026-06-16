def get_prompt(numero_bloques: int, json_conceptos: list[dict]) -> str:
    return f"""
Eres un experto en diseño curricular, organización de contenidos educativos y creación de itinerarios de aprendizaje progresivos.

Tu tarea consiste en organizar una lista de conceptos previamente identificados dentro de un conjunto de bloques de aprendizaje.

Cada bloque representará un nivel dentro de un juego educativo.

El objetivo es crear una progresión lógica, comprensible y gradual para el estudiante.

## Objetivo

Distribuye los conceptos en hasta {numero_bloques} bloques de aprendizaje.
Puedes usar menos bloques si la estructura pedagógica lo requiere, pero nunca más.

La agrupación debe favorecer una progresión natural desde los conceptos más generales hasta los más específicos.

Información sobre los conceptos

Cada concepto contiene:
	- nombre
	- descripción
	- nivel
	- depende_de

El campo depende_de indica los conceptos que deben comprenderse previamente para entender correctamente dicho concepto.

## Reglas obligatorias
1. Todos los conceptos deben aparecer exactamente una vez.
2. Ningún concepto puede repetirse.
3. Todos los conceptos deben ser asignados a un bloque.
4. Los bloques deben seguir un orden de menor a mayor dificultad.
5. Respeta las dependencias del campo depende_de.
6. Un concepto no puede aparecer antes que otro del que depende.
7. Dentro de cada bloque, respeta el orden de dependencias cuando sea posible.
8. Los bloques deben ser coherentes temáticamente.
9. Evita bloques sin coherencia solo para cumplir número.
10. Los conceptos deben coincidir exactamente con los nombres del input.
11. No incluyas texto fuera del JSON.

## Proceso que debes seguir
1. Analiza todos los conceptos.
2. Identifica relaciones temáticas entre ellos.
3. Analiza las dependencias.
4. Determina un orden lógico de aprendizaje.
5. Agrupa conceptos que pertenezcan al mismo subtema, fenómeno o dominio funcional del conocimiento.
6. Asigna un número secuencial a cada bloque.
7. Genera un título representativo para cada bloque.
8. Genera una descripción breve del contenido del bloque.
9. Devuelve únicamente el JSON solicitado.

## Formato de salida
Devuelve únicamente un objeto JSON válido.
La clave principal debe ser:
```
{
  "bloques": []
}
```

Cada bloque debe tener exactamente la siguiente estructura:
```
{
  "numero": 1,
  "titulo": "Título del bloque",
  "descripcion": "Descripción breve del contenido del bloque",
  "conceptos": [
    "Concepto 1",
    "Concepto 2"
  ]
}
```

## Número de bloques solicitado
{numero_bloques}

## Conceptos a agrupar
{json_conceptos}

## Ejemplo de formato esperado:
{
  "bloques": [
    {
      "numero": 1,
      "titulo": "Introducción al Sistema Solar",
      "descripcion": "Presentación general del Sistema Solar y de sus componentes principales.",
      "conceptos": [
        "Sistema Solar",
        "Sol",
        "Planetas"
      ]
    },
    {
      "numero": 2,
      "titulo": "Planetas interiores",
      "descripcion": "Estudio de los planetas más cercanos al Sol y de sus características fundamentales.",
      "conceptos": [
        "Mercurio",
        "Venus",
        "Tierra",
        "Marte"
      ]
    }
  ]
}
"""