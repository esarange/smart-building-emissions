from typing import Dict, Any
from ..components.base import Component
from ..components.energy import EnergyComponent
from ..components.material import MaterialComponent
from ..components.water import WaterComponent

class ComponentFactory:
    """Factory for creating component instances"""
    
    def create_component(self, component_type: str, name: str, **parameters) -> Component:
        """Create a component instance based on type"""
        component_type = component_type.lower()
        
        if component_type == 'energy':
            return self._create_energy_component(name, **parameters)
        elif component_type == 'material':
            return self._create_material_component(name, **parameters)
        elif component_type == 'water':
            return self._create_water_component(name, **parameters)
        else:
            raise ValueError(f"Unknown component type: {component_type}")
    
    def _create_energy_component(self, name: str, **parameters) -> EnergyComponent:
        """Create an energy component with validated parameters"""
        required_params = ['energy_source', 'efficiency', 'annual_consumption_kwh']
        self._validate_parameters(required_params, parameters)
        
        return EnergyComponent(name, **parameters)
    
    def _create_material_component(self, name: str, **parameters) -> MaterialComponent:
        """Create a material component with validated parameters"""
        required_params = ['material_name']
        self._validate_parameters(required_params, parameters)
        
        return MaterialComponent(name, **parameters)
    
    def _create_water_component(self, name: str, **parameters) -> WaterComponent:
        """Create a water component with validated parameters"""
        required_params = ['annual_consumption_liters']
        self._validate_parameters(required_params, parameters)
        
        return WaterComponent(name, **parameters)
    
    def _validate_parameters(self, required_params: list, parameters: Dict[str, Any]) -> None:
        """Validate that all required parameters are present"""
        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
    
    def get_component_template(self, component_type: str) -> Dict[str, Any]:
        """Get a template of required parameters for a component type"""
        templates = {
            'energy': {
                'description': 'Energy consumption system',
                'required_parameters': ['energy_source', 'efficiency', 'annual_consumption_kwh'],
                'example': {
                    'energy_source': 'electricity',
                    'efficiency': 0.85,
                    'annual_consumption_kwh': 50000
                }
            },
            'material': {
                'description': 'Building material',
                'required_parameters': ['material_name'],
                'example': {
                    'material_name': 'concrete',
                    'density_kg_m3': 2400,
                    'volume_m3': 100
                }
            },
            'water': {
                'description': 'Water consumption system',
                'required_parameters': ['annual_consumption_liters'],
                'example': {
                    'annual_consumption_liters': 100000,
                    'water_treatment_factor': 0.8
                }
            }
        }
        
        return templates.get(component_type.lower(), {})