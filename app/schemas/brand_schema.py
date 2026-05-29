from pydantic import BaseModel


class BrandResponse(BaseModel):
    name: str
    logo: str
    description: str


class CreateBrandRequest(BaseModel):
    name: str
    description: str