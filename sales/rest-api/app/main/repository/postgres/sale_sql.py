"""Sales SQL Statements."""

FIELD_COUNT = 10

FIELDS = (
    "id, date_time, order_id, sku, quantity, subtotal, fee, "
    "tax, created_at, updated_at"
)

PARAMETERS = ("%s, " * FIELD_COUNT)[:-2]

SELECT_SALE_BY_ID_STATEMENT = (
    f"SELECT {FIELDS} FROM sale WHERE id = %s LIMIT 1"
)

INSERT_SALE_STATEMENT = f'INSERT INTO "sale" ({FIELDS}) VALUES ({PARAMETERS})'

DELETE_SALE_BY_ID_STATEMENT = 'DELETE FROM "sale" WHERE id = %s'

SELECT_SALES_AFTER_STATEMENT = (
    f'SELECT {FIELDS} FROM "sale" WHERE created_at <= (SELECT created_at '
    'FROM "sale" WHERE id = %(id)s) AND id <> %(id)s ORDER BY created_at '
    "DESC LIMIT %(limit)s"
)

SELECT_SALES_BEFORE_STATEMENT = (
    f'SELECT * FROM (SELECT {FIELDS} FROM "sale" WHERE created_at >= '
    '(SELECT created_at FROM "sale" WHERE id = %(id)s) AND id <> %(id)s '
    'ORDER BY created_at ASC LIMIT %(limit)s) AS "filtered_sales" ORDER '
    "BY created_at DESC"
)


def generate_update_sale_statement(fields):
    """Generate statement for updating sale."""
    query = 'UPDATE "sale" SET '
    for f in fields:
        query += f + " = (%s), "
    query = query[:-2] + " WHERE id = (%s)"
    return query
