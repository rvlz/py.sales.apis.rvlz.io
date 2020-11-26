"""Fixtures."""
from datetime import datetime

import pytest


@pytest.fixture
def sale():
    return {
        "id": "123",
        "date_time": datetime.utcnow(),
        "order_id": "FFX",
        "sku": "ff-11-22",
        "quantity": 32,
        "subtotal": 50000,
        "fee": 1200,
        "tax": 1555,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
