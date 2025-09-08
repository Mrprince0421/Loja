from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
import DB, security, schemas, models

router = APIRouter(prefix='/products', tags=['products'])

T_Session = Annotated[Session, Depends(DB.get_session)]
T_CurrentUser = Annotated[models.User, Depends(security.get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=schemas.ProductPublic
)
def create_product(
        product: schemas.ProductSchema, session: T_Session, current_user: T_CurrentUser
):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        QT=product.QT
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.get('/', response_model=list[schemas.ProductPublic])
def read_products(
        session: T_Session,
        skip: int = 0,
        limit: int = 100,
        name: str | None = Query(None),
        product_id: int | None = Query(None)
):
    query = select(models.Product)
    if name:
        query = query.where(models.Product.name.contains(name))
    if product_id:
        query = query.where(models.Product.id == product_id)

    products = session.scalars(query.offset(skip).limit(limit)).all()

    if not products:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product(s) not found"
        )

    return products


@router.put('/{product_id}', response_model=schemas.ProductPublic)
def update_product(
        product_id: int,
        product: schemas.ProductUpdateSchema,
        session: T_Session,
        current_user: T_CurrentUser
):
    db_product = session.scalar(select(models.Product).where(models.Product.id == product_id))
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete(
    '/{product_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None
)
def delete_product(
    product_id: int, session: T_Session, current_user: T_CurrentUser
):
    db_product = session.scalar(select(models.Product).where(models.Product.id == product_id))
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    session.delete(db_product)
    session.commit()
    return None