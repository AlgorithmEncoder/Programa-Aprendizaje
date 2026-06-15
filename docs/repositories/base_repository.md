
# BaseRepository

## 📌 Propósito

Clase base que abstrae el acceso a SQLite.

Todos los repositories heredan de esta clase.

---

## 🧱 Funciones internas

### _fetchone_raw()

Ejecuta SELECT y devuelve una fila.

### _fetchall_raw()

Ejecuta SELECT y devuelve múltiples filas.

### _execute()

Ejecuta INSERT / UPDATE / DELETE.

---

## 🔄 Responsabilidad

- Manejo de conexión
- Ejecución SQL
- Commit automático

---

## ❌ NO hace

- No convierte a models
- No contiene lógica de negocio