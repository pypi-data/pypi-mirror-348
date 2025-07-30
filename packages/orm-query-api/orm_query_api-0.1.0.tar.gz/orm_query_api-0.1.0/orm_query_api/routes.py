# routes.py
from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from typing import Annotated, Type
from sqlalchemy.exc import NoResultFound
from sqlalchemy import exists
from starlette.responses import Response
from .services.db_services import get_session
from .parser.query_parser import parse_query
from .parser.query_validation import validate_query_options
from .parser.query_parse import get_all
from .services.serialization import BaseSerializer
from pydantic import BaseModel


def generate_crud_router(model: type, serializer: Type[BaseSerializer], prefix: str,
                         pydantic_model: Type[BaseModel]) -> APIRouter:
    router = APIRouter(prefix=f"/{prefix}", tags=[prefix])
    session = get_session()

    @router.get("/")
    async def list_items(request: Request):
        query_options = parse_query(request.url.query)
        validate_query_options(query_options, serializer)
        query = get_all(query_options, serializer)
        return Response(content=session.scalar(query), media_type="application/json")

    @router.get("/{item_id}")
    async def get_one(item_id: Annotated[int, Path(ge=0)]):
        try:
            return session.query(model).filter(model.id == item_id).one()
        except NoResultFound:
            raise HTTPException(status_code=404)

    @router.post("/")
    async def create_item(input_data: pydantic_model):  # user passes correct Pydantic
        db_item = model(**input_data.model_dump())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

    @router.put("/{item_id}")
    async def update_item(item_id: int, input_data: pydantic_model):
        if not session.query(model).filter(model.id == item_id).first():
            raise HTTPException(status_code=404)
        md = input_data.model_dump()
        md.update({"id": item_id})
        db_item = model(**md)
        session.merge(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

    @router.patch("/{item_id}")
    async def partial_update_item(item_id: int, input_data: pydantic_model):
        db_item = session.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404)
        for key, value in input_data.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        session.commit()
        return db_item

    @router.delete("/{item_id}", status_code=204)
    async def delete_item(item_id: int):
        try:
            db_item = session.query(model).filter(model.id == item_id).one()
        except NoResultFound:
            raise HTTPException(status_code=404)
        session.delete(db_item)
        session.commit()

    return router
