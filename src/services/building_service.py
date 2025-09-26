
from typing import List, Dict, Any
from src.data.repositories import (
    BuildingRepository, 
    BuildingResponse, 
    BuildingComponentResponse, 
    BuildingComponentUpdateResponse, 
    ComponentRepository, 
    ComponentsByBuildingRepository
)
from src.core.building import Building
from src.core.factory import ComponentFactory
from src.core.models import (
    BuildingComponentLink, 
    BuildingResponse, 
    BuildingComponentUpdateResponse
)

class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()
        self.component_repo = ComponentRepository()
        self.components_by_building_repo = ComponentsByBuildingRepository()
        self.factory = ComponentFactory()
    
    def create_building(self, name: str, location: str, component_ids_with_quantities: List[BuildingComponentLink] = None) -> BuildingResponse:
        """Create a new building and add components to it"""
        building_data = self.building_repo.create({
            'name': name,
            'location': location
        })

        self.components_by_building_repo.add_components_to_building(building_data['id'], component_ids_with_quantities)
        
        return building_data

    def get_all_buildings(self) -> List[BuildingResponse]:
        return self.building_repo.get_all()
    
    def get_buildings_by_name(self, name: str) -> List[BuildingResponse]:
        return self.building_repo.get_by_name(name)
    
    def get_building(self, building_id: str) -> BuildingResponse:
        return self.building_repo.get_by_id(building_id)

    def get_with_components(self, building_id: str) -> BuildingResponse:
        return self.building_repo.get_with_components(building_id)
    
    def add_component_to_building(self, building_id: str, component_id: str, quantity: int = 1) -> BuildingResponse:
        """Add a component to an existing building"""
        return self.components_by_building_repo.add_component_to_building(building_id, component_id, quantity)
    
    def update_component_quantity(self, building_id: str, component_id: str, quantity: int) -> BuildingComponentUpdateResponse:
        """Update the quantity of a component in a building"""
        return self.components_by_building_repo.update_component_quantity(building_id, component_id, quantity)

    def calculate_building_emissions(self, building_id: str, modifications: Dict[str, Any] = None) -> Dict[str, Any]:
        building_data = self.building_repo.get_with_components(building_id)
        if not building_data:
            raise ValueError(f"Building {building_id} not found")
        
        # Create Building instance
        building = Building(building_data['name'], building_data['location'])
        
        # Add components to building with their quantities
        for component_data in building_data.get('components', []):
            print(f"Component data: {component_data}")
            component = self.factory.create_component(
                component_type=component_data['components']['component_type'],
                name=component_data['components']['name'],
                metadata=component_data['components']['metadata']
            )
            # Use the quantity from the join table, default to 1.0
            quantity = component_data.get('quantity', 1)
            building.add_component(component, quantity)
        
        # Apply real-time modifications (digital twin feature)
        if modifications:
            building.apply_modifications(modifications)
        
        # Calculate total emissions with breakdown
        total_emissions, breakdown = building.calculate_total_emissions()
        
        return {
            'total_emissions': total_emissions,
            'breakdown': breakdown,
            'building_id': building_id,
            'component_count': len(building_data.get('components', [])),
            'modifications_applied': modifications or {}
        }