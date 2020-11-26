"""Sale repository tests."""
import pytest

from app.main.repository import (
    SaleModel,
    RepositoryErr,
    RecordNotFoundErr,
    RecordFieldNullErr,
    RecordFieldDuplicateErr,
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


def test_create(mocker, sale):
    """Create sale."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    repo = provide_sale_repository(conn=mock_conn)
    repo.create(s)
    mock_cursor.execute.assert_called_with(
        (
            'INSERT INTO "sale" (id, date_time, order_id, sku, quantity, '
            "subtotal, fee, tax, created_at, updated_at) VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        ),
        (
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
        ),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@pytest.mark.parametrize(
    "field",
    [
        "id",
        "date_time",
        "order_id",
        "sku",
        "quantity",
        "subtotal",
        "fee",
        "tax",
        "created_at",
        "updated_at",
    ],
)
def test_create_null_field_value(mocker, sale, field):
    """Raise 'RecordFieldNullErr' when null constraint violated."""

    class StubNullViolation(Exception):
        """Stub for psycopg2 NotNullViolation exception."""

        class StubDiag:
            def __init__(self, column_name):
                self.column_name = column_name

        def __init__(self, column):
            self.diag = self.StubDiag(column_name=column)

    sale[field] = None
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [StubNullViolation(column=field)]
    repo = provide_sale_repository(conn=mock_conn, null_err=StubNullViolation)
    with pytest.raises(RecordFieldNullErr) as excinfo:
        repo.create(s)
    assert excinfo.value.field == field
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@pytest.mark.parametrize(
    "field,constraint",
    [
        ("id", "sale_pkey"),
    ],
)
def test_create_duplicate_field_value(mocker, sale, field, constraint):
    """Raise 'RecordFieldDuplicateErr' when uniqueness constraint violated."""

    class StubUniqueViolation(Exception):
        """Stub for psycopg2 UniqueViolation exception."""

        class StubDiag:
            def __init__(self, constraint_name):
                self.constraint_name = constraint_name

        def __init__(self, constraint):
            self.diag = self.StubDiag(constraint_name=constraint)

    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [
        StubUniqueViolation(constraint=constraint)
    ]
    repo = provide_sale_repository(
        conn=mock_conn, duplicate_err=StubUniqueViolation
    )
    with pytest.raises(RecordFieldDuplicateErr) as excinfo:
        repo.create(s)
    assert excinfo.value.field == field
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_create_cursor_error(mocker, sale):
    """Raise 'RepositoryErr' exception if cursor exception raise."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_conn.cursor.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.create(s)
    mock_conn.commit.assert_called_once()


def test_create_execute_error(mocker, sale):
    """Raise 'RepositoryErr' exception if query execution raises exception."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.create(s)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
