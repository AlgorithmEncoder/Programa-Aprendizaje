# Modelo: Conocimiento

## 📌 Propósito

Representa una relación conceptual entre dos ideas dentro del contenido educativo.

---

## 🧱 Estructura

```python
Conocimiento(
    id: int | None,
    bloque_id: int,
    temario_id: int | None,
    concepto_a: str,
    tipo_relacion: str | None,
    relacion: str,
    concepto_b: str,
    explicacion: str | None,
    nivel_dificultad: int,
    orden_aprendizaje: int
)
```

---

## 📂 Campos
| Campo         | Tipo | Descripción      |
| ------------- | ---- | ---------------- |
| concepto_a    | str  | Primer concepto  |
| relacion      | str  | Relación lógica  |
| concepto_b    | str  | Segundo concepto |
| tipo_relacion | str  | Tipo semántico   |
| explicacion   | str  | Explicación IA   |

---

## 🔄 Flujo
- Generado desde temarios.
- Base para preguntas.

---

## 🔗 Relaciones
- N Conocimientos → 1 Bloque
- N Conocimientos → 1 Temario
- 1 Conocimiento → N Preguntas
