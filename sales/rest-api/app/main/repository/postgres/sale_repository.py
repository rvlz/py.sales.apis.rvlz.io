"""Postgres Sale Repository."""
from app.main import repository as repo
from app.main.repository.postgres import sale_sql as sql
from app.main.repository import utils


def provide_sale_repository(conn):
    """Initialize and return repository."""
    return SaleRepository(conn=conn)


class SaleRepository(repo.SaleRepository):
    """Sale repository postgres implementation."""

    _cols = (
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
    )

    def __init__(self, conn):
        """Inject connection."""
        self._conn = conn

    def close(self) -> None:
        """Close connection."""
        self._conn.close()

    def find_by_id(self, id: str) -> repo.SaleModel:
        """Find a single sale by id."""
        cur = None
        try:
            cur = self._conn.cursor()
            cur.execute(sql.SELECT_SALE_BY_ID_STATEMENT, (id,))
            row = cur.fetchone()
        except Exception:
            raise repo.RepositoryErr()
        else:
            if row is None:
                raise repo.RecordNotFoundErr()
            return repo.SaleModel(**utils.row_to_dict(self._cols, row))
        finally:
            self._conn.commit()
            if cur is not None:
                cur.close()
