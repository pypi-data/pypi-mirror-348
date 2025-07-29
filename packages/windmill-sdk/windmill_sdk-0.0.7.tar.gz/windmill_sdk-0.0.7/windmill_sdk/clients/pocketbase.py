import httpx
from typing import List, Optional
from ..models import Tenant, Owner, Customer
from .base_client import BaseTenantClient


class PocketBaseClient(BaseTenantClient):
    def __init__(self, base_url: str, username: str, password: str, timeout: int = 10):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.token: Optional[str] = None
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def authenticate(self):
        response = await self.client.post(
            "/api/admins/auth-with-password",
            json={"identity": self.username, "password": self.password},
        )
        response.raise_for_status()
        self.token = response.json()["token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    async def list_tenants(self, filters: Optional[dict] = None) -> List[Tenant]:
        await self.authenticate()

        allowed_fields = {"identifier", "uuid"}
        if filters:
            invalid_fields = set(filters.keys()) - allowed_fields
            if invalid_fields:
                raise ValueError(
                    f"Filtro non valido per i campi: {', '.join(invalid_fields)}. "
                    f"I campi ammessi sono: {', '.join(allowed_fields)}"
                )
            clauses = [f"{key}='{value}'" for key, value in filters.items()]
            filter_str = " && ".join(clauses)
        else:
            filter_str = None

        tenants = []
        page = 1
        per_page = 50

        while True:
            params = {"page": page, "perPage": per_page}
            if filter_str:
                params["filter"] = filter_str

            response = await self.client.get(
                "/api/collections/sdc_tenants/records", params=params
            )
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            tenants.extend([Tenant.model_validate(item) for item in items])

            if page >= data.get("totalPages", 1):
                break
            page += 1

        return tenants

    async def list_tenants_by_owner(
        self, owner_name: Optional[str] = None, owner_identifier: Optional[str] = None
    ) -> List[Tenant]:
        await self.authenticate()

        if bool(owner_name) == bool(owner_identifier):
            raise ValueError(
                "Devi specificare solo uno tra owner_name o owner_identifier."
            )

        org_filter = (
            f"name='{owner_name}'" if owner_name else f"identifier='{owner_identifier}'"
        )
        response = await self.client.get(
            "/api/collections/organizations/records",
            params={"filter": org_filter, "perPage": 1},
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        if not items:
            raise ValueError(f"Nessuna organization trovata con filtro: {org_filter}")

        Owner.model_validate(items[0])
        owner_id = items[0]["id"]

        tenants = []
        page = 1
        while True:
            params = {"page": page, "perPage": 50, "filter": f"owner='{owner_id}'"}
            response = await self.client.get(
                "/api/collections/sdc_tenants/records", params=params
            )
            response.raise_for_status()
            data = response.json()
            tenants.extend(
                [Tenant.model_validate(item) for item in data.get("items", [])]
            )
            if page >= data.get("totalPages", 1):
                break
            page += 1

        return tenants

    async def list_tenants_by_customer(self, customer_name: str) -> List[Tenant]:
        await self.authenticate()

        if not customer_name:
            raise ValueError("Devi specificare un customer_name")

        response = await self.client.get(
            "/api/collections/customers/records",
            params={"filter": f"name='{customer_name}'", "perPage": 1},
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        if not items:
            raise ValueError(f"Nessun customer trovato con name='{customer_name}'")

        Customer.model_validate(items[0])
        customer_id = items[0]["id"]

        tenants = []
        page = 1
        while True:
            params = {
                "page": page,
                "perPage": 50,
                "filter": f"customer='{customer_id}'",
            }
            response = await self.client.get(
                "/api/collections/sdc_tenants/records", params=params
            )
            response.raise_for_status()
            data = response.json()
            tenants.extend(
                [Tenant.model_validate(item) for item in data.get("items", [])]
            )
            if page >= data.get("totalPages", 1):
                break
            page += 1

        return tenants

    async def close(self):
        await self.client.aclose()
