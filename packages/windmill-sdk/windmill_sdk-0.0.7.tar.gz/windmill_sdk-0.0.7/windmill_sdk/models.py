from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, ConfigDict


class Tenant(BaseModel):
    identifier: str
    production_url: HttpUrl
    uuid: UUID
    owner: str
    customer: str

    model_config = ConfigDict(extra="ignore")


class Owner(BaseModel):
    name: str
    identifier: str

    model_config = ConfigDict(extra="ignore")


class Customer(BaseModel):
    name: str

    model_config = ConfigDict(extra="ignore")


class Service(BaseModel):
    id: UUID
    name: str
    slug: str
    tenant: UUID
    identifier: Optional[str] = None

    model_config = {"extra": "ignore"}
