from typing import Optional, Generic, TypeVar, Type

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import update, literal_column

from psycopg2.errors import UniqueViolation

from ..database import get_session

from pydantic import BaseModel
from ..database import Base



ParentModelType = TypeVar("ParentModelType", bound=Base)
DependentModelType = TypeVar("DependentModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDependentService(Generic[ParentModelType, DependentModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def set_model(self, parent_model: Type[ParentModelType], dependent_model: Type[DependentModelType]):
        self.parent_model = parent_model
        self.dependent_model = dependent_model

    def set_parent_column(self, parent_column: str):
        self.parent_column = literal_column(parent_column)

    def _get_parent(self, parent_id: int) -> Optional[ParentModelType]:
        db_obj = (
            self.session.query(self.parent_model)
                .filter(self.parent_model.id == parent_id)
                .first()
        )

        if not db_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{parent_id=} not found")
        return db_obj

    def get(self, parent_id: int, id: int) -> Optional[DependentModelType]:
        db_obj = (
            self.session.query(self.dependent_model)
                .filter(self.dependent_model.id == id)
                .filter(self.parent_column == parent_id)
                .first()
        )

        if not db_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id=} not found")
        return db_obj

    def get_many(self, parent_id: int) -> list[DependentModelType]:
        self._get_parent(parent_id)

        db_objs = (
            self.session.query(self.dependent_model)
                .filter(self.parent_column == parent_id)
                .all()
        )

        return db_objs

    def create(self, parent_id: int, obj_in: CreateSchemaType) -> DependentModelType:
        self._get_parent(parent_id)

        db_obj = self.dependent_model(**obj_in.dict())
        setattr(db_obj, self.parent_column.name, parent_id)

        self.session.add(db_obj)
        try:
            self.session.commit()

        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise HTTPException(status_code=409, detail=str(err.orig))
            raise HTTPException(status_code=400, detail=str(err.args))

        # db_customer = get_customers_by_name(db, name=customer.name)
        # if db_customer:
        #     raise HTTPException(status_code=400, detail="Заказчик с таким название уже есть")

        return db_obj

    def update(self, parent_id: int, id: int, obj_in: UpdateSchemaType, ) -> DependentModelType:
        db_obj = self.get(parent_id, id)

        # new_customer = update(models.Customer).where(models.Customer.id == customer_id).values(**customer_data.dict())
        # self.session.execute(new_customer)
        for field, value in obj_in.dict(exclude_unset=True).items():  # skip_defaults
            setattr(db_obj, field, value)

        try:
            self.session.commit()
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err.args))

        return db_obj

    def delete(self, parent_id: int, id: int, ):
        db_obj = self.get(parent_id, id)
        self.session.delete(db_obj)
        try:
            self.session.commit()
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err.args))
