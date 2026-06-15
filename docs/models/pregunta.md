# Modelo: Pregunta

## 📌 Propósito

Representa una pregunta generada a partir de un conocimiento.

---

## 🧱 Estructura

```python
Pregunta(
    id: int | None,
    conocimiento_id: int,
    tipo: str,
    pregunta: str
)
```

---

## 📂 Campos
| Campo    | Tipo | Descripción          |
| -------- | ---- | -------------------- |
| tipo     | str  | Tipo de pregunta     |
| pregunta | str  | Texto de la pregunta |

---

## 🔄 Flujo
- Generada desde conocimientos.
- Base para respuestas.

---

## 🔗 Relaciones
- N Preguntas → 1 Conocimiento
- 1 Pregunta → N Respuestas