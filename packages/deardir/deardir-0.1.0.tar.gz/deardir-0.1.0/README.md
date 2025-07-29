# deardir

**Validate and optionally create project directory structures from JSON or YAML schema files.**

---

## 🚀 Features

- Validate file/folder structures using declarative schema files
- Supports `.json`, `.yaml`, `.yml`, Python `dict` or `list` objects
- Optionally auto-creates missing directories and files
- Async live mode to continuously monitor a structure
- Python API and CLI interface

---

## 📦 Installation

```bash
pip install deardir
```

Or if you are developing locally:

```bash
poetry install
```

---

## 🧪 Example Schema

### `schema.yml`

```yaml
- data
- src:
    - __init__.py
    - main.py
    - utils:
        - helpers.py
- README.md
- pyproject.toml
```

---

## 🧰 Usage

### Python

```python
from deardir import DearDir
from pathlib import Path

dd = DearDir(root_paths=[Path(".")], schema=Path("schema.yml"))
dd.create_missing = True
dd.validate()

print(dd.missing)   # Set of missing paths
print(dd.created)   # Set of paths that were created
```

### Async live mode

```python
import asyncio

dd = DearDir([Path(".")], "schema.yml")
dd.create_missing = True

asyncio.run(dd.live(interval=10, duration=60))
```

---

### CLI

```bash
deardir check . --schema schema.yml
deardir watch . --schema schema.yml --interval 10 --create
```

---

## 📄 License

MIT
