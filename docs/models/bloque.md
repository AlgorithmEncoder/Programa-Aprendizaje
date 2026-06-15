# Modelo: Bloque

## 📌 Propósito

Representa una subdivisión de un tema.

---

## 🧱 Estructura

```python
Bloque(
    id: int | None,
    tema_id: int,
    numero: int,
    titulo: str,
    descripcion: str | None
)
```

---

## 📂 Campos
| Campo       | Tipo | Descripción           |
| ----------- | ---- | --------------------- |
| id          | int  | Identificador         |
| tema_id     | int  | Tema al que pertenece |
| numero      | int  | Orden dentro del tema |
| titulo      | str  | Título del bloque     |
| descripcion | str  | Descripción opcional  |

---

## 🔄 Flujo
- Divide el tema en partes lógicas.
- Alimenta fases posteriores de generación IA.

---

## 🔗 Relaciones
- N Bloques → 1 Tema
- 1 Bloque → N Temarios / Conocimientos