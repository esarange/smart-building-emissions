from typing import Dict, Any, List, Tuple
from ..components.base import Component

class EmissionsCalculator:
    """Core calculator engine for emissions calculations"""
    
    def __init__(self):
        self.emission_factors: Dict[str, float] = {}
    
    def calculate_component_emissions(self, component: Component, quantity: float = 1.0) -> float:
        """Calculate emissions for a single component"""
        return component.calculate_emissions(quantity)
    
    def calculate_building_emissions(self, components: List[Tuple[Component, float]]) -> Tuple[float, Dict[str, Any]]:
        """Calculate total emissions for a list of components"""
        total_emissions = 0.0
        breakdown = {}
        
        for component, quantity in components:
            emissions = self.calculate_component_emissions(component, quantity)
            total_emissions += emissions
            breakdown[component.name] = {
                'emissions': emissions,
                'quantity': quantity,
                'type': component.component_type
            }
        
        return round(total_emissions, 2), breakdown
    
    def compare_scenarios(self, scenario1: Dict[str, Any], scenario2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two emission scenarios"""
        emissions1 = scenario1.get('total_emissions', 0)
        emissions2 = scenario2.get('total_emissions', 0)
        
        difference = emissions2 - emissions1
        percentage_change = (difference / emissions1 * 100) if emissions1 > 0 else 0
        
        return {
            'scenario1_emissions': emissions1,
            'scenario2_emissions': emissions2,
            'absolute_difference': round(difference, 2),
            'percentage_change': round(percentage_change, 2),
            'improvement': difference < 0  # True if scenario2 is better
        }
    
    def calculate_savings_potential(self, current_emissions: float, 
                                  improvement_scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate potential savings for different improvement scenarios"""
        results = []
        
        for scenario in improvement_scenarios:
            potential_emissions = scenario.get('potential_emissions', current_emissions)
            savings = current_emissions - potential_emissions
            savings_percentage = (savings / current_emissions * 100) if current_emissions > 0 else 0
            
            results.append({
                'scenario_name': scenario.get('name', 'Unknown'),
                'current_emissions': current_emissions,
                'potential_emissions': potential_emissions,
                'savings': round(savings, 2),
                'savings_percentage': round(savings_percentage, 2),
                'payback_period': scenario.get('payback_period', 'Unknown')
            })
        
        return sorted(results, key=lambda x: x['savings'], reverse=True)
    
    def validate_component_parameters(self, component: Component) -> bool:
        """Validate that a component has all required parameters"""
        try:
            # Try to calculate emissions - if it fails, parameters are invalid
            test_calculation = component.calculate_emissions(1.0)
            return test_calculation >= 0
        except Exception:
            return False