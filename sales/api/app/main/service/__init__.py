"""Service."""
from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod


class SaleModel:
    """Sale model."""

    def __init__(
        self,
        id: Optional[str] = None,
        date_time: Optional[datetime] = None,
        order_id: Optional[str] = None,
        sku: Optional[str] = None,
        quantity: Optional[int] = None,
        subtotal: Optional[int] = None,
        fee: Optional[int] = None,
        tax: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.date_time = date_time
        self.order_id = order_id
        self.sku = sku
        self.quantity = quantity
        self.subtotal = subtotal
        self.fee = fee
        self.tax = tax
        self.created_at = created_at
        self.updated_at = updated_at


class SaleService(ABC):
    """Sale service interface."""

    @abstractmethod
    def find_by_id(self, id: str) -> SaleModel:
        pass

    @abstractmethod
    def create(self, sale: SaleModel) -> SaleModel:
        pass


class ServiceErr(Exception):
    """Generic service error."""


class ResourceNotFoundErr(ServiceErr):
    """Resource not found."""


class ResourceFieldNullErr(ServiceErr):
    """Resource field cannot be null."""

    def __init__(self, field):
        self.field = field
