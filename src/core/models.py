from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ComponentType(str, Enum):
    ENERGY = "energy"
    MATERIAL = "material"
    WATER = "water"
    TRANSPORT = "transport"

class ComponentBase(BaseModel):
    name: str
    component_type: ComponentType
    metadata: Dict[str, Any]

class ComponentCreate(ComponentBase):
    pass

class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ComponentResponse(ComponentBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ComponentCalculationRequest(BaseModel):
    component_id: str
    quantity: int = 1

class BatchCalculationRequest(BaseModel):
    components: List[ComponentCalculationRequest]

class BuildingBase(BaseModel):
    name: str
    location: Optional[str] = None

class BuildingComponentLink(BaseModel):
    component_id: str
    quantity: int = 1

class BuildingCreate(BaseModel):
    name: str
    location: Optional[str] = None
    components: List[BuildingComponentLink] = []

class BuildingComponentResponse(BaseModel):
    component: ComponentResponse
    quantity: int 

class BuildingComponentUpdate(BaseModel):
    quantity: int

class BuildingComponentUpdateResponse(BaseModel):
    component: ComponentResponse
    quantity: int

class BuildingResponse(BuildingBase):
    id: str
    components: List[BuildingComponentResponse] = []
    created_at: datetime

class EmissionCalculationRequest(BaseModel):
    building_id: str
    modifications: Dict[str, Any] = {}