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

class EmissionFactorCategory(str, Enum):
    MATERIAL = "material"
    ENERGY = "energy"
    WATER = "water"
    TRANSPORT = "transport"

class EmissionFactorBase(BaseModel):
    name: str
    category: EmissionFactorCategory
    emission_factor: float
    unit: str
    source: Optional[str] = None

class EmissionFactorCreate(EmissionFactorBase):
    pass

class EmissionFactorUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[EmissionFactorCategory] = None
    emission_factor: Optional[float] = None
    unit: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None

class EmissionFactorResponse(EmissionFactorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmissionFactorSearch(BaseModel):
    category: Optional[EmissionFactorCategory] = None
    name_contains: Optional[str] = None
    min_factor: Optional[float] = None
    max_factor: Optional[float] = None