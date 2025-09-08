from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
import DB, security, schemas, models
from security import get_current_user
from datetime import date, datetime

router = APIRouter(prefix='/sales', tags=['sales'])
T_Session = Annotated[Session, Depends(DB.get_session)]
T_CurrentUser = Annotated[models.User, Depends(security.get_current_user)]


@router.get('/daily_report', response_model=schemas.DailySales)
def get_daily_sales_report(session: T_Session, current_user: T_CurrentUser):
    today = date.today()

    total_sales_count = session.query(models.Sale).filter(
        func.date(models.Sale.created_at) == today
    ).count()

    total_sales_amount = session.query(func.sum(models.Sale.total_price)).filter(
        func.date(models.Sale.created_at) == today
    ).scalar() or 0

    return schemas.DailySales(total_sales=total_sales_count, total_amount=total_sales_amount)


@router.post(
    '/create-payment', status_code=HTTPStatus.OK, response_model=dict
)
def create_payment(
        sale: schemas.SaleSchema,
        session: T_Session,
        current_user: T_CurrentUser
):
    total_price = 0

    for item in sale.items:
        product = session.scalar(
            select(models.Product).where(models.Product.id == item.product_id)
        )

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Produto com ID {item.product_id} não encontrado'
            )

        if product.QT < item.QT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Produto {product.name} não tem estoque suficiente.'
            )

        total_price += product.price * item.QT

    qr_code_data = {
        'payment_id': 'PAY_12345',
        'qr_code_base64': 'simulacao-de-qr-code-para-pagamento',
        'total_price': total_price,
    }

    return qr_code_data


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=schemas.SalePublic
)
def create_sale(
        sale: schemas.SaleSchema,
        session: T_Session,
        current_user: T_CurrentUser
):
    total_price = 0
    sale_items = []

    for item in sale.items:
        product = session.scalar(
            select(models.Product).where(models.Product.id == item.product_id)
        )

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Produto com ID {item.product_id} não encontrado'
            )
        if product.QT < item.QT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Produto {product.name} não tem estoque suficiente.'
            )

        product.QT -= item.QT
        session.add(product)

        sale_item = models.SaleItem(
            sale_id=0,
            product_id=product.id,
            QT=item.QT,
            product_price=product.price
        )
        sale_items.append(sale_item)
        total_price += product.price * item.QT

    db_sale = models.Sale(
        user_id=current_user.id,
        total_price=total_price
    )
    session.add(db_sale)
    session.commit()
    session.refresh(db_sale)

    for item in sale_items:
        item.sale_id = db_sale.id
        session.add(item)

    session.commit()
    session.refresh(db_sale)

    return db_sale