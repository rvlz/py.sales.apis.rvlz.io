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
