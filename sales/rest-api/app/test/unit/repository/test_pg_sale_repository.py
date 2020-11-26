"""Sale repository tests."""
import pytest

from app.main.repository import (
    SaleModel,
    RepositoryErr,
    RecordNotFoundErr,
)
from app.main.repository.postgres.sale_repository import (
    provide_sale_repository,
)


def test_find_by_id(mocker, sale):
    """Retrieves a sale by id."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    repo = provide_sale_repository(conn=mock_conn)
    mock_cursor.fetchone.return_value = (
        sale["id"],
        sale["date_time"],
        sale["order_id"],
        sale["sku"],
        sale["quantity"],
        sale["subtotal"],
        sale["fee"],
        sale["tax"],
        sale["created_at"],
        sale["updated_at"],
    )
    s = repo.find_by_id(sale["id"])
    mock_cursor.execute.assert_called_with(
        (
            "SELECT id, date_time, order_id, sku, quantity, subtotal, fee, "
            "tax, created_at, updated_at FROM sale WHERE id = %s LIMIT 1"
        ),
        (sale["id"],),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    assert isinstance(s, SaleModel)
    assert s.id == sale["id"]
    assert s.date_time == sale["date_time"]
    assert s.order_id == sale["order_id"]
    assert s.sku == sale["sku"]
    assert s.quantity == sale["quantity"]
    assert s.subtotal == sale["subtotal"]
    assert s.fee == sale["fee"]
    assert s.tax == sale["tax"]
    assert s.created_at == sale["created_at"]
    assert s.updated_at == sale["updated_at"]


def test_find_by_id_not_found(mocker, sale):
    """Raise 'RecordNotFoundErr' exception when sale not found."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = None
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RecordNotFoundErr):
        repo.find_by_id(sale["id"])
    mock_cursor.execute.assert_called_with(
        (
            "SELECT id, date_time, order_id, sku, quantity, subtotal, fee, "
            "tax, created_at, updated_at FROM sale WHERE id = %s LIMIT 1"
        ),
        (sale["id"],),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_find_by_id_cursor_error(mocker, sale):
    """Raise 'RepositoryErr' exception when cursor raises exception."""
    mock_conn = mocker.Mock()
    mock_conn.cursor.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.find_by_id(sale["id"])
    mock_conn.commit.assert_called_once()


def test_find_by_id_execute_error(mocker, sale):
    """
    Raise 'RepositoryErr' exception when query execution raises exception.
    """
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.find_by_id(sale["id"])
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
