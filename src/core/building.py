from typing import List, Dict, Any, Tuple
from ..components.base import Component

class Building:
    """Digital twin representation of a building"""
    
    def __init__(self, name: str, location: str = None):
        self.name = name
        self.location = location
        self.components: List[Tuple[Component, float]] = []  # (component, quantity)
        self.modifications: Dict[str, Any] = {}
    
    def add_component(self, component: Component, quantity: float = 1.0) -> None:
        """Add a component to the building with specified quantity"""
        self.components.append((component, quantity))
    
    def remove_component(self, component_name: str) -> bool:
        """Remove a component by name"""
        for i, (component, quantity) in enumerate(self.components):
            if component.name == component_name:
                self.components.pop(i)
                return True
        return False
    
    def apply_modifications(self, modifications: Dict[str, Any]) -> None:
        """Apply real-time modifications to components (digital twin feature)"""
        self.modifications = modifications
        
        # Apply modifications to relevant components
        for component, quantity in self.components:
            component_mods = modifications.get(component.name, {})
            if component_mods:
                component.update_parameters(component_mods)
    
    def calculate_total_emissions(self) -> Tuple[float, Dict[str, Any]]:
        """Calculate total emissions with breakdown by component"""
        total_emissions = 0.0
        breakdown = {}
        
        for component, quantity in self.components:
            try:
                component_emissions = component.calculate_emissions(quantity)
                total_emissions += component_emissions
                breakdown[component.name] = {
                    'emissions': component_emissions,
                    'quantity': quantity,
                    'type': component.component_type,
                    'percentage': 0  # Will be calculated after total
                }
            except Exception as e:
                print(f"Error calculating emissions for {component.name}: {e}")
                breakdown[component.name] = {
                    'emissions': 0,
                    'quantity': quantity,
                    'type': component.component_type,
                    'error': str(e)
                }
        
        # Calculate percentages
        if total_emissions > 0:
            for component_data in breakdown.values():
                if 'emissions' in component_data and component_data['emissions'] > 0:
                    component_data['percentage'] = round(
                        (component_data['emissions'] / total_emissions) * 100, 2
                    )
        
        return round(total_emissions, 2), breakdown
    
    def get_component_count(self) -> int:
        """Get the number of components in the building"""
        return len(self.components)
    
    def get_components_by_type(self, component_type: str) -> List[Tuple[Component, float]]:
        """Get all components of a specific type"""
        return [(comp, qty) for comp, qty in self.components if comp.component_type == component_type]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert building to dictionary for serialization"""
        return {
            'name': self.name,
            'location': self.location,
            'component_count': self.get_component_count(),
            'modifications': self.modifications
        }
    
    def __str__(self) -> str:
        return f"Building('{self.name}', {self.get_component_count()} components)"
    
    def __repr__(self) -> str:
        return f"Building(name='{self.name}', location='{self.location}')"