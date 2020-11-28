"""Sale service test."""
import pytest

from app.main import repository as rp
from app.main import service as srv
from app.main.service.sale_service import provide_sale_service


def test_find_by_id(mocker, sale):
    """Find a single sale by id."""
    repo_s = rp.SaleModel(**sale)
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = repo_s
    service = provide_sale_service(repository=mock_repo)
    s = service.find_by_id(id=sale["id"])
    assert isinstance(s, srv.SaleModel)
    assert s.id == repo_s.id
    assert s.date_time == repo_s.date_time
    assert s.order_id == repo_s.order_id
    assert s.sku == repo_s.sku
    assert s.quantity == repo_s.quantity
    assert s.subtotal == repo_s.subtotal
    assert s.fee == repo_s.fee
    assert s.tax == repo_s.tax
    assert s.created_at == repo_s.created_at
    assert s.updated_at == repo_s.updated_at
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
