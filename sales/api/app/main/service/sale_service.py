"""Sale service."""
from app.main import service as srv
from app.main import repository as repo
from app.main.helper import mapper


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
