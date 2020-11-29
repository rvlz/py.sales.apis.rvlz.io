"""Sale service."""
import copy
from datetime import datetime
from typing import List

from app.main import service as srv
from app.main import repository as repo
from app.main.helper import mapper
from app.main.service import utils


def provide_sale_service(repository: repo.SaleRepository):
    """Initialize and return service."""
    return SaleService(repository=repository)


class SaleService(srv.SaleService):
    """Sale service implementation."""

    def __init__(self, repository: repo.SaleRepository):
        """Inject repository."""
        self._repository = repository

    def find_by_id(self, id: str) -> srv.SaleModel:
        """Find single sale by id."""
        try:
            s = self._repository.find_by_id(id)
            sale = mapper.to_sale_service_model(s)
            return sale
        except repo.RecordNotFoundErr:
            raise srv.ResourceNotFoundErr()
        except Exception:
            raise srv.ServiceErr()

    def create(self, sale: srv.SaleModel) -> srv.SaleModel:
        """Create a sale."""
        try:
            new_service_sale = copy.copy(sale)
            new_service_sale.id = utils.generate_id()
            new_service_sale.created_at = datetime.utcnow()
            new_service_sale.updated_at = datetime.utcnow()
            repo_sale = mapper.to_sale_repo_model(new_service_sale)
            self._repository.create(repo_sale)
            return new_service_sale
        except repo.RecordFieldNullErr as error:
            raise srv.ResourceFieldNullErr(field=error.field)
        except Exception:
            raise srv.ServiceErr()

    def delete_by_id(self, id: str) -> None:
        """Delete sale by id."""
        try:
            self._repository.delete_by_id(id)
        except repo.RecordNotFoundErr:
            raise srv.ResourceNotFoundErr()
        except Exception:
            raise srv.ServiceErr()

    def update(self, sale: srv.SaleModel, fields: List[str]) -> None:
        """Update sale."""
        try:
            repo_sale = mapper.to_sale_repo_model(sale)
            self._repository.update(repo_sale, fields)
        except repo.RecordNotFoundErr:
            raise srv.ResourceNotFoundErr()
        except repo.RecordFieldNullErr as error:
            raise srv.ResourceFieldNullErr(field=error.field)
        except ValueError:
            raise srv.InvalidArgsErr()
        except Exception:
            raise srv.ServiceErr()

    def find(
        self,
        id: str,
        limit: int = 10,
        after: bool = True,
    ) -> List[srv.SaleModel]:
        try:
            results = self._repository.find(id, limit, after)
            return [mapper.to_sale_service_model(r) for r in results]
        except ValueError:
            raise srv.InvalidArgsErr()
        except Exception:
            raise srv.ServiceErr()
