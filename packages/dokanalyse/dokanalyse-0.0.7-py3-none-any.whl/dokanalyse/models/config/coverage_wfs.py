from typing import List
from pydantic import BaseModel, HttpUrl
import uuid


class CoverageWfs(BaseModel):
    url: HttpUrl
    layer: str
    geom_field: str
    property: str
    planning_guidance_id: uuid.UUID = None
    building_guidance_id: uuid.UUID = None
    properties: List[str] = []    
