from typing import Dict, Any
from ..components.base import Component
from ..components.energy import EnergyComponent
from ..components.material import MaterialComponent
from ..components.water import WaterComponent

class ComponentFactory:
    """Factory for creating component instances"""
    
    def create_component(self, component_type: str, name: str, **metadata) -> Component:
        """Create a component instance based on type"""
        component_type = component_type.lower()
        
        if component_type == 'energy':
            return self._create_energy_component(name, **metadata)
        elif component_type == 'material':
            return self._create_material_component(name, **metadata)
        elif component_type == 'water':
            return self._create_water_component(name, **metadata)
        else:
            raise ValueError(f"Unknown component type: {component_type}")
    
    def _create_energy_component(self, name: str, **metadata) -> EnergyComponent:
        """Create an energy component with validated metadata"""
        required_params = ['energy_source', 'efficiency', 'annual_consumption_kwh']
        self._validate_metadata(required_params, metadata['metadata'])
        
        return EnergyComponent(name, **metadata)
    
    def _create_material_component(self, name: str, **metadata) -> MaterialComponent:
        """Create a material component with validated metadata"""
        required_params = ['material_name', 'density_kg_m3', 'volume_m3']
        self._validate_metadata(required_params, metadata['metadata'])
        
        return MaterialComponent(name, **metadata)
    
    def _create_water_component(self, name: str, **metadata) -> WaterComponent:
        """Create a water component with validated metadata"""
        required_params = ['annual_consumption_liters', 'water_treatment_factor', 'treatment_type']
        self._validate_metadata(required_params, metadata['metadata'])
        
        return WaterComponent(name, **metadata)
    
    def _validate_metadata(self, required_params: list, metadata: Dict[str, Any]) -> None:
        """Validate that all required metadata are present"""
        missing_params = [param for param in required_params if param not in metadata]
        if missing_params:
            raise ValueError(f"Missing required metadata: {missing_params}")
    
    def get_component_template(self, component_type: str) -> Dict[str, Any]:
        """Get a template of required metadata for a component type"""
        templates = {
            'energy': {
                'description': 'Energy consumption system',
                'required_metadata': ['energy_source', 'efficiency', 'annual_consumption_kwh'],
                'example': {
                    'energy_source': 'electricity',
                    'efficiency': 0.85,
                    'annual_consumption_kwh': 50000
                }
            },
            'material': {
                'description': 'Building material',
                'required_metadata': ['material_name', 'density_kg_m3', 'volume_m3'],
                'example': {
                    'material_name': 'concrete',
                    'density_kg_m3': 2400,
                    'volume_m3': 100
                }
            },
            'water': {
                'description': 'Water consumption system',
                'required_metadata': ['annual_consumption_liters', 'water_treatment_factor', 'treatment_type'],
                'example': {
                    'annual_consumption_liters': 100000,
                    'water_treatment_factor': 0.8,
                    'treatment_type': 'standard'
                }
            }
        }
        
        return templates.get(component_type.lower(), {})