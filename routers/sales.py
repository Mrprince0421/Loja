from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
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
        and_(
            func.date(models.Sale.created_at) == today,
            models.Sale.user_id == current_user.id
        )
    ).count()

    total_sales_amount = session.query(func.sum(models.Sale.total_price)).filter(
        and_(
            func.date(models.Sale.created_at) == today,
            models.Sale.user_id == current_user.id
        )
    ).scalar() or 0

    return schemas.DailySales(total_sales=total_sales_count, total_amount=total_sales_amount)


@router.get(
    '/report_by_period',
    response_model=schemas.SalesByPeriodReport
)
def get_sales_by_period(
        session: T_Session,
        current_user: T_CurrentUser,
        start_date: date,
        end_date: date
):
    query = (
        select(
            models.Sale.created_at.label('sale_date'),
            models.SaleItem.QT.label('quantity_sold'),
            models.Product.name.label('product_name'),
            models.SaleItem.product_price.label('total_price')
        )
        .join(models.Sale)
        .join(models.Product)
        .where(
            and_(
                models.Sale.created_at >= start_date,
                models.Sale.created_at <= end_date,
                models.Sale.user_id == current_user.id
            )
        )
        .order_by(models.Sale.created_at)
    )

    sales_data = session.execute(query).all()

    report_items = [
        schemas.SaleItemReport(
            product_name=item.product_name,
            quantity_sold=item.quantity_sold,
            sale_date=item.sale_date,
            total_price=item.total_price
        )
        for item in sales_data
    ]

    return schemas.SalesByPeriodReport(sales=report_items)


@router.get(
    '/best_selling',
    response_model=schemas.BestSellingProductsReport
)
def get_best_selling_products(
        session: T_Session,
        current_user: T_CurrentUser,
        limit: int = Query(10, gt=0, le=100)
):
    query = (
        select(
            models.Product.id,
            models.Product.name,
            func.sum(models.SaleItem.QT).label('total_quantity_sold'),
            func.sum(models.SaleItem.QT * models.SaleItem.product_price).label('total_revenue')
        )
        .join(models.SaleItem, models.Product.id == models.SaleItem.product_id)
        .join(models.Sale, models.SaleItem.sale_id == models.Sale.id)
        .where(models.Sale.user_id == current_user.id)
        .group_by(models.Product.id, models.Product.name)
        .order_by(func.sum(models.SaleItem.QT).desc())
        .limit(limit)
    )

    best_sellers = session.execute(query).all()

    report_products = [
        schemas.BestSellingProduct(
            product_id=item.id,
            product_name=item.name,
            total_quantity_sold=item.total_quantity_sold,
            total_revenue=item.total_revenue
        )
        for item in best_sellers
    ]

    return schemas.BestSellingProductsReport(products=report_products)


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
            select(models.Product).where(
                models.Product.id == item.product_id,
                models.Product.user_id == current_user.id
            )
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
            select(models.Product).where(
                models.Product.id == item.product_id,
                models.Product.user_id == current_user.id
            )
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