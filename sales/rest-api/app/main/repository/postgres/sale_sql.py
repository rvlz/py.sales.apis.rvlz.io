"""Sales SQL Statements."""

FIELDS = (
    "id, date_time, order_id, sku, quantity, subtotal, fee, "
    "tax, created_at, updated_at"
)

SELECT_SALE_BY_ID_STATEMENT = (
    f"SELECT {FIELDS} FROM sale WHERE id = %s LIMIT 1"
)
