"""
Example
# main.py

from fastapi import FastAPI
from your_package.registry import model_registry
from your_package.models import User
# Optionally from your_package.serializers import UserSerializer

app = FastAPI()

# Auto-generated serializer
model_registry.register_model(User)

# Or with custom serializer
# model_registry.register_model(User, serializer_class=UserSerializer)

model_registry.register_all_routes(app)

"""
from typing import Type, Optional, Dict
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from .routes import generate_crud_router
from .services.serialization import BaseSerializer
from .utils.auto_gen import create_schema_and_serializer


class ModelRegistry:
    def __init__(self):
        self.registry: Dict[str, Dict] = {}
        self.router = APIRouter()

    def register_model(
            self,
            model: type,
            serializer_class: Optional[Type[BaseSerializer]] = None,
            prefix: Optional[str] = None,
            pydantic_model: Optional[Type[BaseModel]] = None,
            auto_generate: bool = False,
    ):
        """
        Registers a model with optional custom serializer.
        If serializer_class is not provided, it is auto-generated.
        """
        if auto_generate or serializer_class is None or pydantic_model is None:
            pydantic_model, serializer_class = create_schema_and_serializer(model)

        model_name = model.__name__
        route_prefix = prefix or model_name.lower()

        self.registry[model_name] = {
            "model": model,
            "serializer": serializer_class,
            "prefix": route_prefix,
            "pydantic_model": pydantic_model,
        }

        router = generate_crud_router(
            model=model,
            serializer=serializer_class,
            prefix=route_prefix,
            pydantic_model=pydantic_model
        )
        self.router.include_router(router)

    def register_all_routes(self, app: FastAPI):
        """
        Include all registered routes in the FastAPI app.
        """
        app.include_router(self.router)


# Global registry instance
model_registry = ModelRegistry()
