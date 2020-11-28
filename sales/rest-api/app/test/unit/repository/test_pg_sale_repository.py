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


def test_delete_by_id(mocker, sale):
    """Delete sale by id."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.rowcount = 1
    repo = provide_sale_repository(conn=mock_conn)
    repo.delete_by_id(sale["id"])
    mock_cursor.execute.assert_called_with(
        'DELETE FROM "sale" WHERE id = %s',
        (sale["id"],),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_delete_by_id_no_found(mocker, sale):
    """Raise 'RecordNotFoundErr' when sale not found."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.rowcount = 0
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RecordNotFoundErr):
        repo.delete_by_id(sale["id"])
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_delete_by_id_cursor_error(mocker, sale):
    """Raise 'RepositoryErr' when cursor exception raised."""
    mock_conn = mocker.Mock()
    mock_conn.cursor.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.delete_by_id(sale["id"])
    mock_conn.commit.assert_called_once()


def test_delete_by_id_execute_error(mocker, sale):
    """Raise 'RepositoryErr' when query execution raises exception."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.delete_by_id(sale["id"])
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@pytest.mark.parametrize(
    "query,fields",
    [
        ('UPDATE "sale" SET order_id = (%s) WHERE id = (%s)', ["order_id"]),
        (
            'UPDATE "sale" SET '
            "order_id = (%s), "
            "date_time = (%s), "
            "sku = (%s) "
            "WHERE id = (%s)",
            ["order_id", "date_time", "sku"],
        ),
        (
            'UPDATE "sale" SET '
            "order_id = (%s), "
            "date_time = (%s), "
            "sku = (%s), "
            "quantity = (%s) "
            "WHERE id = (%s)",
            ["order_id", "date_time", "sku", "quantity"],
        ),
    ],
)
def test_update(mocker, sale, query, fields):
    """Update sale."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    repo = provide_sale_repository(conn=mock_conn)
    repo.update(s, fields)
    mock_cursor.execute.assert_called_with(
        query,
        tuple(sale[f] for f in (fields + ["id"])),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@pytest.mark.parametrize(
    "fields", [["foo", "bar"], ["foobar"], ["foobar", "sku"]]
)
def test_update_invalid_fields(mocker, sale, fields):
    """Raises 'ValueError' exception when invalid fields provided."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(ValueError) as excinfo:
        repo.update(s, fields)
    excinfo.value.args == (f'"{fields[0]}" not valid field.',)


def test_update_empty_fields(mocker, sale):
    """Raises 'ValueError' exception when empty list of fields provided."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(ValueError) as excinfo:
        repo.update(s, [])
    assert excinfo.value.args == ('"fields" argument cannot be empty list.',)


@pytest.mark.parametrize(
    "fields",
    (
        ["id"],
        ["sku", "id"],
        ["order_id", "sku", "id"],
    ),
)
def test_update_id_field(mocker, sale, fields):
    """Raises 'ValueError' exception when id provided in fields list."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(ValueError) as excinfo:
        repo.update(s, fields)
    assert excinfo.value.args == ('"id" cannot be changed.',)


def test_update_null_id(mocker, sale):
    """Raises 'ValueError' exception when sale.id is None."""
    s = SaleModel(**sale)
    s.id = None
    mock_conn = mocker.Mock()
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(ValueError) as excinfo:
        repo.update(s, ["sku"])
    assert excinfo.value.args == ('Instance attribute "id" cannot be None.',)


@pytest.mark.parametrize(
    "field",
    [
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
def test_update_null_field_value(mocker, sale, field):
    """Raise 'RecordFieldNullErr' exception when null constraint violated."""

    class StubNullViolation(Exception):
        """Stub for psycopg2 NotNullViolation exception."""

        class StubDiag:
            def __init__(self, column_name):
                self.column_name = column_name

        def __init__(self, column):
            self.diag = self.StubDiag(column_name=column)

    s = SaleModel(**sale)
    setattr(s, field, None)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [StubNullViolation(column=field)]
    repo = provide_sale_repository(conn=mock_conn, null_err=StubNullViolation)
    with pytest.raises(RecordFieldNullErr) as excinfo:
        repo.update(s, [field])
    assert excinfo.value.field == field
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_update_cursor_error(mocker, sale):
    """Raise 'RepositoryErr' when cursor exception raised."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_conn.cursor.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.update(s, ["sku"])
    mock_conn.commit.assert_called_once()


def test_update_execute_error(mocker, sale):
    """Raise 'RepositoryErr' when query execution raises exception."""
    s = SaleModel(**sale)
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.update(s, ["sku"])
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


@pytest.mark.parametrize("count", [10])
def test_find_after(mocker, sale_rows, count):
    """
    Find sales that come after a certain sale when ordered by
    descending "created_at" time.
    """
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = sale_rows
    repo = provide_sale_repository(conn=mock_conn)
    sales = repo.find(id="1", limit=count, after=True)
    mock_cursor.execute.assert_called_with(
        "SELECT id, date_time, order_id, sku, quantity, subtotal, "
        'fee, tax, created_at, updated_at FROM "sale" '
        'WHERE created_at <= (SELECT created_at FROM "sale" '
        "WHERE id = %(id)s) AND id <> %(id)s ORDER BY created_at "
        "DESC LIMIT %(limit)s",
        {"id": "1", "limit": count},
    )
    mock_cursor.close.assert_called_once()
    assert isinstance(sales, list)
    assert len(sales) == count
    for s in sales:
        assert isinstance(s, SaleModel)


@pytest.mark.parametrize("count", [10])
def test_find_before(mocker, sale_rows, count):
    """
    Find sale that come before a certain sale when ordered by
    descending "created_at" time.
    """
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = sale_rows
    repo = provide_sale_repository(conn=mock_conn)
    sales = repo.find(id="1", limit=count, after=False)
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM (SELECT id, date_time, order_id, sku, quantity, "
        'subtotal, fee, tax, created_at, updated_at FROM "sale" WHERE '
        'created_at >= (SELECT created_at FROM "sale" WHERE id = %(id)s) '
        "AND id <> %(id)s ORDER BY created_at ASC LIMIT %(limit)s) AS "
        '"filtered_sales" ORDER BY created_at DESC',
        {"id": "1", "limit": count},
    )
    mock_cursor.close.assert_called_once()
    assert isinstance(sales, list)
    assert len(sales) == count
    for s in sales:
        assert isinstance(s, SaleModel)


@pytest.mark.parametrize("limit", [-30, 0, 101])
def test_find_invalid_limit(mocker, limit):
    """
    Raises ValueError exception when limit is less than 1
    or greater than 100.
    """
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value.fetchall.return_value = []
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(ValueError) as excinfo:
        repo.find("1", limit=limit)
    assert excinfo.value.args == (
        '"limit" argument must be between 1 and 100 inclusive.',
    )


def test_find_cursor_error(mocker):
    """Raise custom exception when cursor exception raised."""
    mock_conn = mocker.Mock()
    mock_conn.cursor.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.find("1")
    mock_conn.commit.assert_called_once()


def test_find_execute_error(mocker):
    """Raise custom exception when query execution exception raised."""
    mock_conn = mocker.Mock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.side_effect = [Exception()]
    repo = provide_sale_repository(conn=mock_conn)
    with pytest.raises(RepositoryErr):
        repo.find("1")
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
