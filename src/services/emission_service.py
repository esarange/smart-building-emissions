from src.data.repositories import ComponentRepository
from src.core.factory import ComponentFactory
from typing import List, Dict, Any, Optional, List
from src.core.models import (
    EmissionFactorCategory, 
    EmissionFactorResponse
)

class EmissionService:
    def __init__(self):
        self.component_repo = ComponentRepository()
        self.factory = ComponentFactory()
    
    def calculate_component_emissions(self, component_id: str, quantity: float = 1.0) -> float:
        """Calculate emissions for a single component"""
        component_data = self.component_repo.get_by_id(component_id)
        if not component_data:
            raise ValueError(f"Component {component_id} not found")
        
        component = self.factory.create_component(
            component_type=component_data['component_type'],
            name=component_data['name'],
            **component_data['parameters']
        )
        return component.calculate_emissions(quantity)