"""Fixtures."""
import datetime as dt
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


@pytest.fixture
def sale_rows(count):
    return [
        (
            str(i),
            datetime.utcnow() + dt.timedelta(minutes=i),
            f"FFX{i}",
            f"ff-11-22-{i}",
            10 + i,
            1000 + i,
            10 + i,
            100 + i,
            datetime.utcnow() + dt.timedelta(minutes=i),
            datetime.utcnow() + dt.timedelta(minutes=i),
        )
        for i in range(count)
    ]
