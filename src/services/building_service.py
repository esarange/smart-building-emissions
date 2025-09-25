
from typing import List, Dict, Any
from src.data.repositories import BuildingRepository, ComponentRepository
from src.core.building import Building
from src.core.factory import ComponentFactory

class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()
        self.component_repo = ComponentRepository()
        self.factory = ComponentFactory()
    
    def create_building(self, name: str, location: str, component_ids: List[int] = None) -> Dict[str, Any]:
        """Create a new building and add components to it"""
        building_data = self.building_repo.create({
            'name': name,
            'location': location
        })
        
        return building_data
    
    def add_component_to_building(self, building_id: int, component_id: int, quantity: int = 1) -> dict:
        """Add a component to an existing building"""
        return self.building_repo.add_component(building_id, component_id, quantity)
    
    def calculate_building_emissions(self, building_id: int, modifications: Dict[str, Any] = None) -> Dict[str, Any]:
        building_data = self.building_repo.get_with_components(building_id)
        if not building_data:
            raise ValueError(f"Building {building_id} not found")
        
        # Create Building instance
        building = Building(building_data['name'], building_data['location'])
        
        # Add components to building with their quantities
        for component_data in building_data.get('components', []):
            component = self.factory.create_component(
                component_type=component_data['component_type'],
                name=component_data['name'],
                **component_data['metadata']
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