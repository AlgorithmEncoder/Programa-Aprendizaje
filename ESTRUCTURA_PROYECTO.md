# Estructura del proyecto

## Objetivo

Este proyecto genera automáticamente contenido educativo mediante la API de ChatGPT para construir una base de datos de aprendizaje utilizada por un juego educativo.

El flujo general es:

Tema
→ Esquematización
→ Agrupación
→ Temario
→ Conocimientos
→ Preguntas
→ Respuestas incorrectas

---

# Estructura de carpetas

```text
proyecto/

│
├── main.py
│
├── config/
│   └── settings.py
│
├── database/
│   ├── db.py
│   ├── db_setup.py
│   └── repositories/
│       ├── temas_repository.py
│       ├── bloques_repository.py
│       ├── temarios_repository.py
│       ├── conocimientos_repository.py
│       ├── preguntas_repository.py
│       └── generaciones_repository.py
│
├── ai/
│   ├── client.py
│   ├── prompts/
│   │   ├── fase1_esquematizacion.py
│   │   ├── fase2_agrupacion.py
│   │   ├── fase3_temario.py
│   │   ├── fase4_conocimientos.py
│   │   ├── fase5_preguntas.py
│   │   └── fase6_respuestas_incorrectas.py
│   │
│   └── generators/
│       ├── fase1_generator.py
│       ├── fase2_generator.py
│       ├── fase3_generator.py
│       ├── fase4_generator.py
│       ├── fase5_generator.py
│       └── fase6_generator.py
│
├── validators/
│   ├── fase1_validator.py
│   ├── fase2_validator.py
│   ├── fase3_validator.py
│   ├── fase4_validator.py
│   ├── fase5_validator.py
│   └── fase6_validator.py
│
├── services/
│   ├── generation_service.py
│   ├── tema_service.py
│   └── recovery_service.py
│
├── models/
│   ├── tema.py
│   ├── bloque.py
│   ├── temario.py
│   ├── conocimiento.py
│   └── pregunta.py
│
├── logs/
│
├── docs/
│
├── README.md
└── ESTRUCTURA_PROYECTO.md
```

---

# Descripción de carpetas

## config/

Contiene toda la configuración global del proyecto.

### settings.py

Configuración de:

- Modelo utilizado.
- Temperatura.
- Límites de conocimientos.
- Límites de preguntas.
- Parámetros generales del sistema.

---

## database/

Contiene todo el acceso a la base de datos.

### db.py

Gestión de conexiones SQLite.

### db_setup.py

Creación y validación de tablas.

---

## database/repositories/

Acceso a cada tabla.

Cada repositorio contiene operaciones CRUD específicas.

### temas_repository.py

Gestión de temas.

### bloques_repository.py

Gestión de bloques.

### temarios_repository.py

Gestión de temarios.

### conocimientos_repository.py

Gestión de conocimientos.

### preguntas_repository.py

Gestión de preguntas.

### generaciones_repository.py

Histórico de ejecuciones de cada fase.

---

## ai/

Todo lo relacionado con la inteligencia artificial.

---

### client.py

Cliente único para interactuar con la API de OpenAI.

Responsabilidades:

- Enviar prompts.
- Recibir respuestas.
- Gestionar errores.
- Convertir respuestas a JSON.

---

## ai/prompts/

Contiene los prompts utilizados por cada fase.

### fase1_esquematizacion.py

Prompt de esquematización.

### fase2_agrupacion.py

Prompt de agrupación.

### fase3_temario.py

Prompt de generación de temario.

### fase4_conocimientos.py

Prompt de extracción de conocimientos.

### fase5_preguntas.py

Prompt de generación de preguntas.

### fase6_respuestas_incorrectas.py

Prompt de generación de distractores.

---

## ai/generators/

Implementación de cada fase.

Responsabilidades:

- Construir prompt.
- Llamar a la IA.
- Procesar respuesta.
- Devolver JSON.

---

## validators/

Validaciones de salida de la IA.

Cada fase dispone de su propio validador.

Responsabilidades:

- Comprobar estructura.
- Detectar duplicados.
- Comprobar coherencia.
- Validar reglas de negocio.

---

## services/

Lógica principal del sistema.

### generation_service.py

Orquesta todo el flujo completo.

Ejemplo:

Tema
→ Fase 1
→ Validación
→ Guardado

→ Fase 2
→ Validación
→ Guardado

...

---

### tema_service.py

Operaciones específicas sobre temas.

---

### recovery_service.py

Recuperación de procesos interrumpidos.

Permite continuar una generación desde una fase concreta.

---

## models/

Representaciones lógicas de las entidades.

### tema.py

Modelo Tema.

### bloque.py

Modelo Bloque.

### temario.py

Modelo Temario.

### conocimiento.py

Modelo Conocimiento.

### pregunta.py

Modelo Pregunta.

---

## logs/

Registro de actividad del sistema.

Ejemplos:

- Errores.
- Llamadas a IA.
- Validaciones.
- Costes de generación.

---

## main.py

Punto de entrada principal del proyecto.

Desde aquí se lanzarán las generaciones completas de nuevos temas.

---

# Flujo previsto

```text
Tema
    ↓
Fase 1 - Esquematización
    ↓
Fase 2 - Agrupación
    ↓
Fase 3 - Temario
    ↓
Fase 4 - Conocimientos
    ↓
Fase 5 - Preguntas
    ↓
Fase 6 - Respuestas incorrectas
    ↓
Base de datos
```
