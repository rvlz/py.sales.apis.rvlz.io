"""Postgres Sale Repository."""
from typing import List

import psycopg2

from app.main import repository as repo
from app.main.repository.postgres import sale_sql as sql
from app.main.repository import utils


def provide_sale_repository(
    conn,
    null_err=psycopg2.errors.NotNullViolation,
    duplicate_err=psycopg2.errors.UniqueViolation,
):
    """Initialize and return repository."""
    return SaleRepository(
        conn=conn,
        null_err=null_err,
        duplicate_err=duplicate_err,
    )


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

    def __init__(self, conn, null_err, duplicate_err):
        """Inject connection."""
        self._conn = conn
        self._null_err = null_err
        self._duplicate_err = duplicate_err

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

    def create(self, sale: repo.SaleModel) -> None:
        """Create a sale."""
        cur = None
        try:
            cur = self._conn.cursor()
            cur.execute(
                sql.INSERT_SALE_STATEMENT,
                (
                    sale.id,
                    sale.date_time,
                    sale.order_id,
                    sale.sku,
                    sale.quantity,
                    sale.subtotal,
                    sale.fee,
                    sale.tax,
                    sale.created_at,
                    sale.updated_at,
                ),
            )
        except self._null_err as error:
            column = error.diag.column_name
            raise repo.RecordFieldNullErr(field=column)
        except self._duplicate_err as error:
            constraint = error.diag.constraint_name
            field = utils.field_from_constraint(constraint)
            raise repo.RecordFieldDuplicateErr(field=field)
        except Exception:
            raise repo.RepositoryErr()
        finally:
            self._conn.commit()
            if cur is not None:
                cur.close()

    def delete_by_id(self, id: str) -> None:
        """Delete a sale by id."""
        cur = None
        try:
            cur = self._conn.cursor()
            cur.execute(sql.DELETE_SALE_BY_ID_STATEMENT, (id,))
        except Exception:
            raise repo.RepositoryErr()
        else:
            if cur.rowcount != 1:
                raise repo.RecordNotFoundErr()
        finally:
            self._conn.commit()
            if cur is not None:
                cur.close()

    def update(self, sale: repo.SaleModel, fields: List[str]) -> None:
        """Update a sale."""
        cur = None
        values = utils.extract_update_values(sale, fields)
        try:
            cur = self._conn.cursor()
            stmt = sql.generate_update_sale_statement(fields)
            cur.execute(
                stmt,
                values,
            )
        except self._null_err as error:
            column = error.diag.column_name
            raise repo.RecordFieldNullErr(field=column)
        except Exception:
            raise repo.RepositoryErr()
        finally:
            self._conn.commit()
            if cur is not None:
                cur.close()
