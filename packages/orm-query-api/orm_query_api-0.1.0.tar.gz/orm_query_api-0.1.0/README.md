# orm-query-api

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/github/license/kkommatt/orm-query-api.svg)](LICENSE)

🚀 **orm-query-api** is a modern Python library for dynamically generating RESTful CRUD APIs from SQLAlchemy models using FastAPI — with advanced query parsing, validation, and automatic serialization.

---

## ✨ Features

- ✅ Auto-generate CRUD endpoints for any SQLAlchemy model
- ✅ Supports query string filters, sorting, pagination
- ✅ Typed input via Pydantic models
- ✅ Response serialization using custom serializers
- ✅ Built-in validation and error handling
- ✅ Easily composable into any FastAPI app

---

## 📦 Installation

```bash
pip install orm-query-api
````

> Or add it to your `requirements.txt`.

---

## 🚀 Quick Start

### 1. Define your SQLAlchemy model

```python

import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Date
from sqlalchemy.orm import Mapped, relationship

from orm_query_api.services.db_services import Base
from typing import List

class ToDo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = Column(Integer, primary_key=True)
    comment: Mapped[str] = Column(String, nullable=True, default=None)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    priority: Mapped[int] = Column(Integer)
    is_main: Mapped[bool] = Column(Boolean)
    worker_fullname: Mapped[str] = Column(String)
    due_date: Mapped[datetime.date] = Column(Date)
    count: Mapped[int] = Column(Integer, default=1)
    users: Mapped[List["User"]] = relationship(
        secondary="todo_user", back_populates="todos"
    )
```

### 2. Define your input Pydantic model and serializer

```python
from pydantic import BaseModel
from orm_query_api.services.serialization import BaseSerializer
import datetime
from typing import List
from orm_query_api.services.serialization import SerializerField, RelationField


class ToDoPydantic(BaseModel):
    comment: str | None = None
    created_at: datetime.datetime
    priority: int
    is_main: bool = False
    worker_fullname: str
    due_date: datetime.date
    count: int = 0
    user_ids: List[int]


class ToDoSerializer(BaseSerializer):
    model = ToDo
    fields = [
        SerializerField("id", "primary_key"),
        SerializerField("comment", "instruction"),
        SerializerField("created_at", "creation_time"),
        SerializerField("priority", "preference"),
        SerializerField("is_main", "is_principal"),
        SerializerField("worker_fullname", "worker"),
        SerializerField("due_date", "deadline"),
        SerializerField("count", "amount"),
        RelationField("slaves", "slaves"),
        RelationField("users", "users"),
    ]

```

### 3. Generate and include the router

```python
from fastapi import FastAPI
from orm_query_api.routes import generate_crud_router

app = FastAPI()

todo_router = generate_crud_router(
    model=ToDo,
    serializer=ToDoSerializer,
    pydantic_model=ToDoPydantic,
    prefix="todo"
)

app.include_router(todo_router)
```

---

## 🔍 Advanced Querying

Supports `GET /q=(id, created_at).filter(created_at=2022-01-01).offset(2).limit(10)` style queries with:

* `filter`: field'operator'value
* `order`: `order(field).asc` or `order(field).desc`
* `offset` / `limit`: for pagination
* All parsed and validated against the serializer.

---

## 📁 Project Structure

```bash
orm-query-api/
├── routes.py
├── registry.py
├── utils/
│   ├── __init__.py     
│   └── auto_gen.py        
├── exceptions/
│   ├── __init__.py     
│   └── error.py    
├── parser/
│   ├── query_parser.py     # Parses query strings
│   ├── query_validation.py # Validates parsed query
│   └── query_parse.py      # Generates SQLAlchemy query objects
├── services/
│   ├── db_services.py      # DB session management
│   ├── serialization.py    # BaseSerializer class
│   ├── exc_handlers.py    
│   └── __init__.py    
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

Use `pytest` with coverage:

```bash
pytest --cov=orm_query_api
```

---

## 📚 Roadmap

* [ ] Auto-generate input model from SQLAlchemy models
* [ ] Swagger-compatible filtering/sorting docs
* [ ] Plugin hooks (e.g. auth, caching)
* [ ] Async SQLAlchemy support (SQLModel or 2.0)

---

## 🛠 Dependencies

* FastAPI
* SQLAlchemy
* Pydantic
* Lark for grammar-based query parsing

---

## 👥 Contributing

Contributions are welcome! Feel free to fork, open issues, or submit PRs.

---

## 📄 License

MIT © [kkommatt](https://github.com/kkommatt)
