"""Service."""
from datetime import datetime
from typing import Optional, List
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

    def to_json_dict(self):
        """Convert to JSON serializable dict."""
        return {
            "id": self.id,
            "date_time": self.date_time,
            "order_id": self.order_id,
            "sku": self.sku,
            "quantity": self.quantity,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "fee": self.fee,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class SaleService(ABC):
    """Sale service interface."""

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> SaleModel:
        pass

    @abstractmethod
    def create(self, sale: SaleModel) -> SaleModel:
        pass

    @abstractmethod
    def delete_by_id(self, id: str) -> None:
        pass

    @abstractmethod
    def update(self, sale: SaleModel, fields: List[str]) -> None:
        pass

    @abstractmethod
    def find(
        self,
        id: str,
        limit: int = 10,
        after: bool = True,
    ) -> List[SaleModel]:
        pass


class ServiceErr(Exception):
    """Generic service error."""


class ResourceNotFoundErr(ServiceErr):
    """Resource not found."""


class ResourceFieldNullErr(ServiceErr):
    """Resource field cannot be null."""

    def __init__(self, field):
        self.field = field


class InvalidArgsErr(ServiceErr):
    """Invalid argments."""
