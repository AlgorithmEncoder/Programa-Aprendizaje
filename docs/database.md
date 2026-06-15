# 📚 Base de Datos - Sistema de Aprendizaje

## 📌 Introducción

Esta base de datos está diseñada para soportar un sistema de aprendizaje progresivo basado en generación de contenido, descomposición en bloques, extracción de conocimientos y evaluación mediante preguntas.

El objetivo es modelar un flujo completo de aprendizaje:

> **Tema → Bloques → Temario → Conocimientos → Preguntas → Respuestas**

Además, se registra el proceso de generación del contenido mediante la tabla `generaciones`, permitiendo trazabilidad del sistema de IA.

---

# 🧱 Arquitectura General

La base de datos sigue un modelo relacional jerárquico con separación clara entre:

- Contenido educativo (temas, bloques, temario)
- Representación estructurada del conocimiento
- Evaluación del aprendizaje
- Registro de procesos de generación

---

# 📊 Modelo de Datos

## 1. 📘 Temas

Representa el nivel más alto de organización del conocimiento.

### Propósito
Agrupar el contenido general de estudio.

### Estructura

|     Campo      |    Tipo   |     Descripción     |
|----------------|-----------|---------------------|
|       id       |  INTEGER  | Identificador único |
|     nombre     |   TEXT    |   Nombre del tema   |
|   descripcion  |   TEXT    | Descripción general |
| fecha_creacion | TIMESTAMP |  Fecha de creación  |

---

## 2. 🧩 Bloques

Divide un tema en partes progresivas de aprendizaje.

### Propósito
Permitir aprendizaje incremental (niveles).

### Estructura

|     Campo      |    Tipo   |     Descripción     |
|----------------|-----------|---------------------|
|       id       |  INTEGER  | Identificador único |
|     tema_id    |  INTEGER  | Relación con temas  |
|     numero     |  INTEGER  |   Orden del bloque  |
|     titulo     |   TEXT    |  Título del bloque  |
|   descripcion  |   TEXT    | Descripción general |

### Relaciones
- Muchos bloques pertenecen a un tema
- Eliminación en cascada desde `temas`

---

## 3. 📖 Temario

Contenido textual base de aprendizaje.

### Propósito
Servir como fuente de información para generar conocimientos.

### Estructura

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INTEGER | Identificador |
| bloque_id | INTEGER | Relación con bloque |
| titulo | TEXT | Título del contenido |
| contenido | TEXT | Texto de aprendizaje |
| orden | INTEGER | Orden dentro del bloque |

### Relaciones
- Un bloque puede tener múltiples temarios

---

## 4. 🧠 Conocimientos

Unidad atómica de aprendizaje estructurado.

### Propósito
Convertir contenido en relaciones conceptuales útiles para aprendizaje didáctico.

### Estructura

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INTEGER | Identificador |
| bloque_id | INTEGER | Relación con bloque |
| temario_id | INTEGER | Origen del conocimiento |
| concepto_a | TEXT | Concepto origen |
| tipo_relacion | TEXT | Tipo de relación |
| relacion | TEXT | Relación semántica |
| concepto_b | TEXT | Concepto destino |
| explicacion | TEXT | Explicación didáctica |
| nivel_dificultad | INTEGER | Nivel (1–n) |
| orden_aprendizaje | INTEGER | Secuencia de aprendizaje |

---

## 5. ❓ Preguntas

Generadas a partir de conocimientos.

### Propósito
Evaluar la comprensión del alumno.

### Estructura

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INTEGER | Identificador |
| conocimiento_id | INTEGER | Relación con conocimiento |
| tipo | TEXT | Tipo de pregunta |
| pregunta | TEXT | Enunciado |

### Relaciones
- Cada conocimiento puede generar múltiples preguntas

---

## 6. ✅ Respuestas

Opciones de respuesta asociadas a preguntas.

### Propósito
Permitir evaluación objetiva.

### Estructura

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INTEGER | Identificador |
| pregunta_id | INTEGER | Relación con pregunta |
| texto | TEXT | Texto de respuesta |
| correcta | INTEGER | 0 = falsa / 1 = correcta |

---

## 7. ⚙️ Generaciones

Tabla de control del sistema de IA.

### Propósito
Registrar cada ejecución de generación de contenido.

### Estados posibles

- pendiente
- ejecutando
- completado
- error
- validado

### Estructura

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INTEGER | Identificador |
| tema_nombre | TEXT | Nombre del tema generado |
| fase | TEXT | Fase del pipeline |
| subfase | TEXT | Subproceso interno |
| numero_bloque | INTEGER | Bloque asociado |
| estado | TEXT | Estado del proceso |
| json_entrada | TEXT | Input del modelo |
| json_salida | TEXT | Output del modelo |
| prompt | TEXT | Prompt utilizado |
| modelo | TEXT | Modelo de IA |
| tokens_entrada | INTEGER | Tokens input |
| tokens_salida | INTEGER | Tokens output |
| coste_estimado | REAL | Coste estimado |
| fecha_creacion | TIMESTAMP | Fecha de ejecución |

---

# 🔗 Relaciones Globales

```text
Temas
 └── Bloques
      └── Temario
           └── Conocimientos
                └── Preguntas
                     └── Respuestas

Y en paralelo:

Generaciones (tracking independiente del pipeline IA)
```

---

# ⚙️ Reglas de Diseño
## 1. Integridad referencial
- Uso de FOREIGN KEY en todas las relaciones
- Eliminación en cascada donde aplica

## 2. Separación de responsabilidades
- Contenido educativo ≠ generación IA
- Evaluación separada del contenido

## 3. Escalabilidad
- Permite múltiples preguntas por conocimiento
- Permite múltiples conocimientos por temario
- Permite crecimiento ilimitado de bloques

## 4. Normalización
- No se almacenan listas dentro de campos
- Respuestas separadas de preguntas
- Estructura 1:N bien definida

---

# 🧠 Diseño conceptual

Este sistema está diseñado para:

## ✔ Aprendizaje progresivo

Cada bloque representa un nivel creciente de dificultad.

## ✔ Generación automática

El contenido se genera mediante IA y se rastrea en generaciones.

## ✔ Evaluación estructurada

El conocimiento se convierte en preguntas objetivas.

## ✔ Trazabilidad completa

Cada paso del pipeline es auditado.

---

# 🚀 Flujo del sistema
1. Crear Tema
2. Dividir en Bloques
3. Generar Temario
4. Extraer Conocimientos
5. Generar Preguntas
6. Crear Respuestas
7. Evaluar Usuario
8. Registrar todo en Generaciones

---

# 📌 Notas finales
- El sistema está preparado para crecimiento modular.
- La tabla generaciones permite observabilidad del sistema de IA.
- La estructura favorece gamificación del aprendizaje.
- Es compatible con arquitecturas futuras (API, microservicios, etc.)
