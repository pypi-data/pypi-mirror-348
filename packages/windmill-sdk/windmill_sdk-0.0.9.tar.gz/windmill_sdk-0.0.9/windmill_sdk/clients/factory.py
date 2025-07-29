import os
from typing import Literal, Optional
from .base_client import BaseTenantClient
from .pocketbase import PocketBaseClient
from .directus import DirectusClient


async def get_tenant_client_async(
    source: Optional[Literal["pocketbase", "directus"]] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> BaseTenantClient:
    # Fallback alle variabili d'ambiente
    source = source or os.getenv("TENANT_CLIENT_SOURCE")
    base_url = base_url or os.getenv("TENANT_CLIENT_URL")
    username = username or os.getenv("TENANT_CLIENT_USERNAME")
    password = password or os.getenv("TENANT_CLIENT_PASSWORD")

    if not source or not base_url or not username or not password:
        raise ValueError(
            "Parametri mancanti: specifica source, base_url, username e password, "
            "o definiscili come variabili d'ambiente:"
            " TENANT_CLIENT_SOURCE, TENANT_CLIENT_URL, TENANT_CLIENT_USERNAME, TENANT_CLIENT_PASSWORD."
        )

    if source == "pocketbase":
        client = PocketBaseClient(base_url, username, password)
    elif source == "directus":
        client = DirectusClient(base_url, username, password)
    else:
        raise ValueError(
            f"Sorgente '{source}' non supportata. Usa 'pocketbase' o 'directus'."
        )

    await client.authenticate()
    return client
