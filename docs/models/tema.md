# Modelo: Tema

## 📌 Propósito

Representa un tema educativo dentro del sistema.  
Es la unidad raíz de toda la estructura de aprendizaje.

---

## 🧱 Estructura

```python
Tema(
    id: int | None,
    nombre: str,
    descripcion: str | None
)
```
---

## 📂 Campos
| Campo       | Tipo | Descripción          |
| ----------- | ---- | -------------------- |
| id          | int  | Identificador único  |
| nombre      | str  | Nombre del tema      |
| descripcion | str  | Descripción opcional |

---

## 🔄 Flujo de uso
- Se crea al iniciar un nuevo contenido educativo.
- Contiene múltiples bloques.
- Es el punto de entrada del pipeline IA.

---

## 🔗 Relaciones
1 Tema → N Bloques

---

## ⚠️ Notas
- id puede ser None antes de persistirse.
- No contiene lógica de negocio.