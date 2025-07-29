import httpx
from typing import List, Optional
from .base_client import BaseTenantClient
from ..models import Tenant


class DirectusClient(BaseTenantClient):
    def __init__(self, base_url: str, email: str, password: str, timeout: int = 10):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.timeout = timeout
        self.token: Optional[str] = None
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def authenticate(self):
        response = await self.client.post(
            "/auth/login", json={"email": self.email, "password": self.password}
        )
        response.raise_for_status()
        self.token = response.json()["data"]["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    async def list_tenants(self, filters: Optional[dict] = None) -> List[Tenant]:
        raise NotImplementedError(
            "DirectusClient.list_tenants non è ancora implementato."
        )

    async def list_tenants_by_owner(
        self, owner_name: Optional[str] = None, owner_identifier: Optional[str] = None
    ) -> List[Tenant]:
        raise NotImplementedError(
            "DirectusClient.list_tenants_by_owner non è ancora implementato."
        )

    async def list_tenants_by_customer(self, customer_name: str) -> List[Tenant]:
        raise NotImplementedError(
            "DirectusClient.list_tenants_by_customer non è ancora implementato."
        )

    async def close(self):
        await self.client.aclose()
