import asyncio

import httpx
from typing import List
from ..models import Service


class SDCClient:
    def __init__(self, base_url: str, username: str, password: str, timeout: int = 10):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.token: str | None = None
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def _authenticate(self) -> str:
        response = await self.client.post(
            "/api/auth", json={"username": self.username, "password": self.password}
        )
        response.raise_for_status()
        token = response.json()["token"]
        self.token = token
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        return token

    async def _request_with_retry(
        self, method: str, url: str, **kwargs
    ) -> httpx.Response:
        response: httpx.Response

        try:
            response = await self.client.request(method, url, **kwargs)
            if response.status_code != 200:
                print(f"{method} {url}: {response.status_code}")

            if response.status_code == 401:
                # Token scaduto ➜ rigenerazione e retry
                await self._authenticate()
                response = await self.client.request(method, url, **kwargs)

            elif response.status_code == 429:
                # Troppi tentativi ➜ rispetto del Retry-After
                retry_after = int(response.headers.get("Retry-After", "1"))
                await asyncio.sleep(retry_after)
                response = await self.client.request(method, url, **kwargs)

            elif 500 <= response.status_code < 600:
                # Errore server ➜ 1 retry veloce
                response = await self.client.request(method, url, **kwargs)

            response.raise_for_status()
            return response

        except httpx.HTTPError as e:
            print(f"[SDCClient] Errore durante la richiesta a {url}: {str(e)}")
            raise

    async def list_services(self) -> List[Service]:
        if not self.token:
            await self._authenticate()

        response = await self._request_with_retry("GET", "/api/services")
        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Risposta inattesa: attesa una lista di servizi")

        return [Service.model_validate(item) for item in data]

    async def get_service_by_identifier(self, identifier: str) -> Service:
        if not self.token:
            await self._authenticate()

        response = await self._request_with_retry(
            "GET", "/api/services", params={"identifier": identifier}
        )
        data = response.json()

        if not isinstance(data, list) or not data:
            raise ValueError(f"Nessun servizio trovato con identifier='{identifier}'")

        return Service.model_validate(data[0])

    async def close(self):
        await self.client.aclose()
