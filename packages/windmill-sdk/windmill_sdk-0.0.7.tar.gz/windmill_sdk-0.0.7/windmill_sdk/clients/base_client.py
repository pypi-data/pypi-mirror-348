from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import Tenant


class BaseTenantClient(ABC):

    @abstractmethod
    async def list_tenants(self, filters: Optional[dict] = None) -> List[Tenant]:
        pass

    @abstractmethod
    async def list_tenants_by_owner(
        self, owner_name: Optional[str] = None, owner_identifier: Optional[str] = None
    ) -> List[Tenant]:
        """Recupera i tenant filtrando per owner name o identifier (solo uno)."""
        pass

    @abstractmethod
    async def list_tenants_by_customer(self, customer_name: str) -> List[Tenant]:
        """Recupera i tenant filtrando per customer name."""
        pass

    @abstractmethod
    async def close(self):
        pass
