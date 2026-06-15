# Modelo: Respuesta

## 📌 Propósito

Representa una opción de respuesta a una pregunta.

---

## 🧱 Estructura

```python
Respuesta(
    id: int | None,
    pregunta_id: int,
    texto: str,
    correcta: bool
)
```

---

## 📂 Campos
| Campo    | Tipo | Descripción           |
| -------- | ---- | --------------------- |
| texto    | str  | Texto de la respuesta |
| correcta | bool | Indica si es correcta |

---

## 🔄 Flujo
- Generadas en fase final.
- Usadas en evaluación.

---

## 🔗 Relaciones
- N Respuestas → 1 Pregunta