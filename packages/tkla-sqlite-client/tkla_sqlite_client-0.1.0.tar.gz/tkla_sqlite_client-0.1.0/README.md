# 🐢 tkla_sqlite_client

**Cliente liviano y robusto para trabajar con SQLite usando SQL puro.**

Ideal para microservicios, APIs locales, scripts embebidos o herramientas de línea de comando donde se prefiera control total y bajo acoplamiento.

---

## 🚀 Características

- 📁 Conexión automática con `sqlite3.connect(path)`
- 🛠️ Creación dinámica de tablas desde esquemas tipo `dict`
- 🔄 Operaciones CRUD (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- 🔎 Utilitarios: `exists()` y `count()`
- 🧾 Respuesta unificada como `dict(success, data, message)`
- 🧱 Seguro por diseño: no permite `UPDATE` ni `DELETE` sin `WHERE`
- 🧼 Logging centralizado
- 🚀 Sin ORM ni dependencias adicionales

---

## 📦 Instalación

```bash
pip install tkla_sqlite_client
```

O instalación local:

```bash
git clone https://github.com/LOVENXON/tkla_sqlite_client.git
cd tkla_sqlite_client
pip install -e .
```

---

## ⚙️ Uso Básico

### 1️⃣ Inicializar conexión

```python
from tkla_sqlite_client.core import SQLiteClient
db = SQLiteClient("mi_base.sqlite")
```

### 2️⃣ Crear tablas

```python
from tkla_sqlite_client.builder import create_tables

schema = {
    "usuarios": {
        "id": {"data_type": "INTEGER", "primary_key": True},
        "nombre": {"data_type": "TEXT", "nullable": False},
        "email": {"data_type": "TEXT", "unique": True}
    }
}

create_tables(schema, db)
```

### 3️⃣ CRUD y Consultas

#### ➕ Insertar

```python
db.insert_data({"usuarios": {"nombre": "Ana", "email": "ana@example.com"}})
```

#### 🔍 Consultar

```python
db.select_data({
    "usuarios": {
        "conditions": {"email": "ana@example.com"},
        "columns": ["id", "nombre"]
    }
})
```

#### ✏️ Actualizar

```python
db.update_data({
    "usuarios": {
        "values": {"nombre": "Ana Actualizada"},
        "conditions": {"email": "ana@example.com"}
    }
})
```

#### ❌ Eliminar

```python
db.delete_data({
    "usuarios": {"conditions": {"email": "ana@example.com"}}
})
```

---

## 🔎 Métodos Utilitarios

#### Verificar existencia

```python
db.exists({"usuarios": {"conditions": {"email": "ana@example.com"}}})
```

#### Contar registros

```python
db.count({"usuarios": {"conditions": {}}})
```

---

## 🧹 Buenas Prácticas

- ✅ Usa `db.close()` al finalizar
- ✅ Valida los campos obligatorios manualmente
- ✅ Evita insertar sin campos requeridos

---

## 📄 Licencia

MIT

---

## ✨ Autor

**Lovenson Pierre**  
📧 lovesonpierre25@gmail.com  
🔗 GitHub: [LOVENXON](https://github.com/LOVENXON)