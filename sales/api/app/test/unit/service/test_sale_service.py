"""Sale service test."""
from datetime import datetime

import pytest

from app.main import repository as rp
from app.main import service as srv
from app.main.service.sale_service import provide_sale_service


def test_find_by_id(mocker, sale):
    """Find a single sale by id."""
    repo_sale = rp.SaleModel(**sale)
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = repo_sale
    service = provide_sale_service(repository=mock_repo)
    service_sale = service.find_by_id(id=sale["id"])
    assert isinstance(service_sale, srv.SaleModel)
    assert service_sale.id == repo_sale.id
    assert service_sale.date_time == repo_sale.date_time
    assert service_sale.order_id == repo_sale.order_id
    assert service_sale.sku == repo_sale.sku
    assert service_sale.quantity == repo_sale.quantity
    assert service_sale.subtotal == repo_sale.subtotal
    assert service_sale.fee == repo_sale.fee
    assert service_sale.tax == repo_sale.tax
    assert service_sale.created_at == repo_sale.created_at
    assert service_sale.updated_at == repo_sale.updated_at
    mock_repo.find_by_id.assert_called_with(sale["id"])


def test_find_by_id_not_found(mocker, sale):
    """Raise 'ResourceNotFoundErr' exception when resource not found."""
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.side_effect = [rp.RecordNotFoundErr()]
    service = provide_sale_service(repository=mock_repo)
    with pytest.raises(srv.ServiceErr):
        service.find_by_id(id=sale["id"])
    mock_repo.find_by_id.assert_called_with(sale["id"])


@pytest.mark.parametrize("exception", [rp.RepositoryErr(), Exception()])
def test_find_by_generic_error(mocker, sale, exception):
    """
    Raises 'ServiceErr' exception for all other types of errors
    (not RecordNotFound error).
    """
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.side_effect = [exception]
    service = provide_sale_service(repository=mock_repo)
    with pytest.raises(srv.ServiceErr):
        service.find_by_id(id=sale["id"])
    mock_repo.find_by_id.assert_called_with(sale["id"])


def test_create(mocker, sale):
    """Create single sale."""
    service_sale = srv.SaleModel(**sale)
    service_sale.id = None
    mock_repo = mocker.Mock()
    service = provide_sale_service(repository=mock_repo)
    service_sale_created = service.create(service_sale)
    assert isinstance(service_sale_created.id, str)
    assert isinstance(service_sale_created.created_at, datetime)
    assert isinstance(service_sale_created.updated_at, datetime)
    assert service_sale_created.date_time == sale["date_time"]
    assert service_sale_created.order_id == sale["order_id"]
    assert service_sale_created.sku == sale["sku"]
    assert service_sale_created.quantity == sale["quantity"]
    assert service_sale_created.subtotal == sale["subtotal"]
    assert service_sale_created.tax == sale["tax"]
    assert service_sale_created.fee == sale["fee"]
    mock_repo.create.assert_called_once()


@pytest.mark.parametrize(
    "field",
    [
        "date_time",
        "order_id",
        "sku",
        "quantity",
        "subtotal",
        "tax",
        "fee",
    ],
)
def test_create_null_field(mocker, sale, field):
    """Raise 'ResourceFieldNullErr' exception for nonnullable field."""
    service_sale = srv.SaleModel(**sale)
    mock_repo = mocker.Mock()
    mock_repo.create.side_effect = [rp.RecordFieldNullErr(field=field)]
    service = provide_sale_service(repository=mock_repo)
    with pytest.raises(srv.ResourceFieldNullErr) as excinfo:
        service.create(service_sale)
    assert excinfo.value.field == field


@pytest.mark.parametrize("exception", [rp.RepositoryErr(), Exception()])
def test_create_generic_error(mocker, sale, exception):
    """Raises 'ServiceErr' exception for all other types of errors."""
    service_sale = srv.SaleModel(**sale)
    mock_repo = mocker.Mock()
    mock_repo.create.side_effect = [exception]
    service = provide_sale_service(repository=mock_repo)
    with pytest.raises(srv.ServiceErr):
        service.create(service_sale)
