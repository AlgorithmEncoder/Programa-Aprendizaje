def get_prompt(tema:str, descripcion:str = None) -> str:
    return f"""
    Eres un experto en diseño curricular y estructuración de conocimiento para juegos educativos.

Tu tarea es analizar el tema proporcionado y generar una estructura conceptual completa del contenido que debería aprender un estudiante.

## Instrucciones

1. Genera únicamente los conceptos necesarios para cubrir el tema de forma completa y equilibrada, evitando redundancias y niveles de detalle excesivos.1. Genera una lista de conceptos y subconceptos relevantes para cubrir el tema de forma completa.
  - Los nombres de los conceptos deben ser únicos.

2. Ordena los conceptos desde los más generales a los más específicos.

3. Asigna a cada concepto un nivel numérico de profundidad por jerarquia:
	- 1 = concepto principal o muy general.
	- 2 = concepto intermedio.
	- 3 o más = concepto más específico o detallado.

4. Incluye una descripción breve y clara para cada concepto.

5. Indica las dependencias entre conceptos mediante el campo depende_de, usando los nombres exactos de los conceptos de los que depende.

6. Si un concepto no depende de ninguno, utiliza una lista vacía: [].

7. No añadas texto explicativo fuera del JSON.

## Formato de salida
- No devuelvas markdown o bloques ```json.
- Devuelve únicamente un objeto JSON válido.
- La clave principal debe ser conceptos.
- Cada concepto debe tener exactamente estas claves:
	- nombre
	- descripcion
	- nivel
	- depende_de
(depende_de representa los conceptos que deben comprenderse previamente para entender correctamente el concepto actual.)

## Tema
{tema}

## Descripción del tema
{descripcion}

## Ejemplo de formato esperado:

### Entrada

Tema
Sistema Solar

Descripción del tema
Aprender la composición, estructura y funcionamiento del Sistema Solar.

### Salida:

{
  "conceptos": [
    {
      "nombre": "Sistema Solar",
      "descripcion": "Conjunto formado por el Sol y los cuerpos que orbitan a su alrededor.",
      "nivel": 1,
      "depende_de": []
    },
    {
      "nombre": "Sol",
      "descripcion": "Estrella situada en el centro del Sistema Solar.",
      "nivel": 2,
      "depende_de": ["Sistema Solar"]
    },
    {
      "nombre": "Planetas",
      "descripcion": "Cuerpos celestes que orbitan alrededor del Sol.",
      "nivel": 2,
      "depende_de": ["Sistema Solar"]
    }
  ]
}
"""