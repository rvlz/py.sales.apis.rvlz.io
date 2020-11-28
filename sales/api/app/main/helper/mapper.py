"""Model mappers."""
from app.main import repository as repo
from app.main import service as srv


def to_sale_service_model(sale: repo.SaleModel):
    """Sale repository model to sale service model."""
    return srv.SaleModel(
        id=sale.id,
        date_time=sale.date_time,
        order_id=sale.order_id,
        sku=sale.sku,
        quantity=sale.quantity,
        subtotal=sale.subtotal,
        fee=sale.fee,
        tax=sale.tax,
        created_at=sale.created_at,
        updated_at=sale.updated_at,
    )


def to_sale_repo_model(sale: srv.SaleModel):
    """Sale service model to sale repository model."""
    return repo.SaleModel(
        id=sale.id,
        date_time=sale.date_time,
        order_id=sale.order_id,
        sku=sale.sku,
        quantity=sale.quantity,
        subtotal=sale.subtotal,
        fee=sale.fee,
        tax=sale.tax,
        created_at=sale.created_at,
        updated_at=sale.updated_at,
    )
