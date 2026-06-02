from uuid import UUID

from pydantic import BaseModel


class BrandResponse(BaseModel):
    id: UUID
    name: str
    logo: str
    description: str
    model_config = {
        "from_attributes": True
    }


class CreateBrandRequest(BaseModel):
    name: str
    description: str


class UpdateBrandRequest(BaseModel):
    name: str
    description: str
