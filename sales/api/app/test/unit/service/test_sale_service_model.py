"""Test Sale Service Model."""
from app.main.service import SaleModel


def test_to_json_dict(sale):
    """Convert sale to dict that is JSON serializable."""
    service_sale = SaleModel(**sale)
    service_sale_dict = service_sale.to_json_dict()
    assert isinstance(service_sale_dict, dict)
    assert service_sale_dict["id"] == service_sale.id
    assert service_sale_dict["date_time"] == service_sale.date_time
    assert service_sale_dict["order_id"] == service_sale.order_id
    assert service_sale_dict["sku"] == service_sale.sku
    assert service_sale_dict["quantity"] == service_sale.quantity
    assert service_sale_dict["subtotal"] == service_sale.subtotal
    assert service_sale_dict["tax"] == service_sale.tax
    assert service_sale_dict["fee"] == service_sale.fee
    assert service_sale_dict["created_at"] == service_sale.created_at
    assert service_sale_dict["updated_at"] == service_sale.updated_at
