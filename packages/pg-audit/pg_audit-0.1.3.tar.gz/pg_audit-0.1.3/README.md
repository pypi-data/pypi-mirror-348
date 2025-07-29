# pg-audit

A PostgreSQL audit system for tracking database changes with rich contextual information, featuring seamless Django integration.

---

## ✨ Features

- **Automatic Change Tracking** – PostgreSQL triggers to log all `INSERT`, `UPDATE`, and `DELETE`
- **Rich Context** – Who, when, why, and from where
- **Partitioned Storage** – Time-partitioned audit table
- **Django Integration** – Models, admin, middleware
- **Flexible Configuration** – Track/include/exclude fields, add conditions
- **Performance Optimized** – Minimal database overhead

---

## 📦 Installation

### With `pip`

```bash
pip install pg-audit
```

To include Django support:

```bash
pip install pg-audit[django]
```

---

### With [`uv`](https://github.com/astral-sh/uv)

```bash
uv pip install pg-audit
uv pip install pg-audit[django]
```

---

## 🚀 Quick Start

### 🔧 With Django

1. **Add to `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    # ...
    'pg_audit.integrations.django',
]
```

2. **Add middleware:**

```python
MIDDLEWARE = [
    # ...
    'pg_audit.integrations.django.middleware.RequestIDMiddleware',
    'pg_audit.integrations.django.middleware.PgAuditMiddleware',
]
```

3. **Register models:**

Create a new `audit.py` file inside your Django app (e.g., `yourapp/audit.py`) and register models there:

```python
# yourapp/audit.py

from pg_audit.integrations.django.audit import register
from .models import User

register(User, track_only=["name", "email"])
```

The `pg_audit` integration will automatically discover and execute this file (like `admin.py`), so no need to import it manually.

4. **Run migrations:**

```bash
python manage.py migrate
```

This will create the audit table and set up triggers automatically.

---

### 🧩 Without Django

```python
from pg_audit.schema import generate_auditlog_table_sql
from pg_audit.triggers import generate_trigger_sql
import psycopg

with psycopg.connect("your_connection_string") as conn, conn.cursor() as cursor:
    # Create audit table
    cursor.execute(generate_auditlog_table_sql("auditlog"))

    # Create trigger for a table
    sql = generate_trigger_sql(
        table_name="users",
        track_only=["name", "email"]
    )
    cursor.execute(sql)
    conn.commit()
```

---

## ⚙️ Configuration Examples

### ✅ Track only specific fields

```python
register(User, track_only=["name", "email"])
```

### ❌ Exclude specific fields

```python
register(Product, exclude_fields=["created_at", "updated_at"])
```

### 📐 Add conditions

```python
register(Subscription, log_conditions="NEW.is_active = TRUE")
```

---

## 📚 Adding Context to Changes

### Using decorator:

```python
from pg_audit.context import with_change_reason

@with_change_reason("User requested password reset")
def reset_password(user_id):
    ...
```

### Using context manager:

```python
from pg_audit.context import audit_context

with audit_context.use_change_reason("Bulk update for compliance"):
    ...
```

---

## 📖 Documentation

👉 Full docs at: [https://pg-audit.readthedocs.io/](https://pg-audit.readthedocs.io/)

---

## 🪪 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
