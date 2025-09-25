from typing import List, Dict, Any, Optional
from src.data.repositories import ComponentRepository
from src.core.factory import ComponentFactory
from src.core.models import ComponentType

class ComponentService:
    def __init__(self):
        self.component_repo = ComponentRepository()
        self.factory = ComponentFactory()
    
    def create_component(self, name: str, component_type: ComponentType, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new component definition"""
        # Validate parameters based on component type
        self._validate_metadata(component_type, metadata)
        
        component_data = {
            'name': name,
            'component_type': component_type.value,
            'metadata': metadata
        }
        
        return self.component_repo.create(component_data)
    
    def get_component(self, component_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific component by ID"""
        return self.component_repo.get_by_id(component_id)
    
    def get_components_by_type(self, component_type: ComponentType) -> List[Dict[str, Any]]:
        """Get all components of a specific type"""
        return self.component_repo.get_by_type(component_type.value)
    
    def get_all_components(self) -> List[Dict[str, Any]]:
        """Get all components"""
        return self.component_repo.get_all()
    
    def update_component(self, component_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a component's metadata"""
        component = self.component_repo.get_by_id(component_id)
        if not component:
            raise ValueError(f"Component {component_id} not found")
        
        # Merge updates with existing parameters
        updated_metadata = {**component['metadata'], **updates.get('metadata', {})}
        
        update_data = {}
        if 'name' in updates:
            update_data['name'] = updates['name']
        update_data['metadata'] = updated_metadata
        
        return self.component_repo.update(component_id, update_data)
    
    def delete_component(self, component_id: int) -> bool:
        """Delete a component"""
        result = self.component_repo.delete(component_id)
        return bool(result)
    
    def calculate_component_emissions(self, component_id: int, quantity: int = 1) -> Dict[str, Any]:
        """Calculate emissions for a single component"""
        component_data = self.component_repo.get_by_id(component_id)
        if not component_data:
            raise ValueError(f"Component {component_id} not found")
        
        component = self.factory.create_component(
            component_type=component_data['component_type'],
            name=component_data['name'],
            metadata=component_data['metadata']
        )
        
        emissions = component.calculate_emissions(quantity)
        
        return {
            'component_id': component_id,
            'component_name': component_data['name'],
            'component_type': component_data['component_type'],
            'quantity': quantity,
            'emissions': emissions,
            'unit': 'kg CO₂e'
        }
    
    def get_component_template(self, component_type: ComponentType) -> Dict[str, Any]:
        """Get a template of required parameters for a component type"""
        templates = {
            ComponentType.ENERGY: {
                "description": "Energy consumption system",
                "required_metadata": ["energy_source", "efficiency", "annual_consumption_kwh"],
                "optional_metadata": ["lifespan_years", "maintenance_factor"],
                # "example": {
                #     "energy_source": "electricity",
                #     "efficiency": 0.85,
                #     "annual_consumption_kwh": 50000
                # }
            },
            ComponentType.MATERIAL: {
                "description": "Building material",
                "required_metadata": ["material_name", "density_kg_m3"],
                "optional_metadata": ["recycling_rate", "transport_distance_km"],
                # "example": {
                #     "material_name": "concrete",
                #     "density_kg_m3": 2400
                # }
            },
            ComponentType.WATER: {
                "description": "Water consumption system",
                "required_metadata": ["annual_consumption_liters", "water_treatment_factor"],
                "optional_metadata": ["recycling_rate", "efficiency"],
                # "example": {
                #     "annual_consumption_liters": 100000,
                #     "water_treatment_factor": 0.8
                # }
            },
            ComponentType.TRANSPORT: {
                "description": "Transportation system",
                "required_metadata": ["vehicle_type", "fuel_type", "annual_distance_km"],
                "optional_metadata": ["fuel_efficiency", "load_factor"],
                # "example": {
                #     "vehicle_type": "delivery_truck",
                #     "fuel_type": "diesel",
                #     "annual_distance_km": 20000
                # }
            }
        }
        
        return templates.get(component_type, {})
    
    def _validate_metadata(self, component_type: ComponentType, metadata: Dict[str, Any]) -> None:
        """Validate that required metadata are present for the component type"""
        template = self.get_component_template(component_type)
        required_metadata = template.get('required_metadata', [])
        
        missing_metadata = [param for param in required_metadata if param not in metadata]
        if missing_metadata:
            raise ValueError(f"Missing required metadata for {component_type.value}: {missing_metadata}")
        
        # Type validation can be added here based on component type
        # if component_type == ComponentType.ENERGY:
        #     if 'efficiency' in metadata and not (0 < metadata['efficiency'] <= 1):
        #         raise ValueError("Efficiency must be between 0 and 1")
    
    def search_components(self, query: str, component_type: Optional[ComponentType] = None) -> List[Dict[str, Any]]:
        """Search components by name or metadata"""
        all_components = self.component_repo.get_all()
        results = []
        
        for component in all_components:
            # Filter by type if specified
            if component_type and component['component_type'] != component_type.value:
                continue
            
            # Search in name
            if query.lower() in component['name'].lower():
                results.append(component)
                continue
            
            # Search in metadata
            metadata_str = str(component['metadata']).lower()
            if query.lower() in metadata_str:
                results.append(component)
        
        return results