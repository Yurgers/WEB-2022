from typing import Optional, Generic, TypeVar, Type

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# from psycopg2.errors import UniqueViolation

from ..database import get_session

from pydantic import BaseModel
from ..database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaceService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def set_model(self, model: Type[ModelType]):
        self.model = model

    def _get(self, id: int) -> Optional[ModelType]:
        db_obj = (
            self.session.query(self.model)
                .filter(self.model.id == id)
                .first()
        )
        if not db_obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id=} not found")
        return db_obj

    def get_many(self, skip: int, limit: int, ) -> list[ModelType]:
        db_objs = (
            self.session.query(self.model)
                .offset(skip).limit(limit)
                .all()
        )
        return db_objs

    def get_many_all(self) -> list[ModelType]:
        db_objs = (
            self.session.query(self.model)
                .all()
        )
        return db_objs

    def get(self, id: int) -> ModelType:
        db_obj = self._get(id)
        return db_obj

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
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

    def update(self, id: int, obj_in: UpdateSchemaType, ) -> ModelType:
        db_obj = self._get(id)

        # new_customer = update(models.Customer).where(models.Customer.id == customer_id).values(**customer_data.dict())
        # self.session.execute(new_customer)
        for field, value in obj_in.dict(exclude_unset=True).items():  # skip_defaults
            setattr(db_obj, field, value)

        try:
            self.session.commit()
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err.args))

        return db_obj

    def delete(self, id: int, ):
        db_obj = self._get(id)
        self.session.delete(db_obj)
        try:
            self.session.commit()
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err.args))
