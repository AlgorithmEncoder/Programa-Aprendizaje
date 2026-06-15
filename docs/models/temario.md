# Modelo: Temario

## 📌 Propósito

Representa un contenido educativo estructurado dentro de un bloque.

---

## 🧱 Estructura

```python
Temario(
    id: int | None,
    bloque_id: int,
    titulo: str | None,
    contenido: str,
    orden: int
)
```

---

## 📂 Campos
| Campo     | Tipo | Descripción             |
| --------- | ---- | ----------------------- |
| id        | int  | Identificador           |
| bloque_id | int  | Bloque padre            |
| titulo    | str  | Título opcional         |
| contenido | str  | Texto educativo         |
| orden     | int  | Orden dentro del bloque |


---

## 🔄 Flujo
- Generado en fases intermedias de IA.
- Sirve como base para conocimientos.

---

## 🔗 Relaciones
- N Temarios → 1 Bloque
- 1 Temario → N Conocimientos