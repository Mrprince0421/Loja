# loja/models.py
from datetime import datetime
from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import func, ForeignKey

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[float]
    QT: Mapped[int]


@table_registry.mapped_as_dataclass
class Sale:
    __tablename__ = 'sales'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    total_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class SaleItem:
    __tablename__ = 'sale_items'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey('sales.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    QT: Mapped[int]
    product_price: Mapped[float]