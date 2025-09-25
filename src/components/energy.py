from .base import Component
from typing import Dict, Any

class EnergyComponent(Component):
    """Component for energy consumption systems (HVAC, lighting, etc.)"""
    
    def __init__(self, name: str, energy_source: str, efficiency: float, 
                 annual_consumption_kwh: float, **kwargs):
        super().__init__(name, "energy")
        self.parameters = {
            'energy_source': energy_source,
            'efficiency': efficiency,
            'annual_consumption_kwh': annual_consumption_kwh,
            **kwargs
        }
    
    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate operational emissions for energy consumption"""
        try:
            # Get emission factor for the energy source (would come from database)
            emission_factor = self._get_energy_emission_factor()
            
            # Calculate effective energy consumption considering efficiency
            effective_consumption = (self.parameters['annual_consumption_kwh'] / 
                                   self.parameters['efficiency'])
            
            # Calculate emissions: energy consumption * emission factor * quantity
            emissions = effective_consumption * emission_factor * quantity
            
            # Add embodied emissions if specified
            embodied_emissions = self.parameters.get('embodied_emissions', 0)
            emissions += embodied_emissions * quantity
            
            return round(emissions, 2)
            
        except KeyError as e:
            raise ValueError(f"Missing required parameter for energy calculation: {e}")
        except ZeroDivisionError:
            raise ValueError("Efficiency cannot be zero")
    
    def _get_energy_emission_factor(self) -> float:
        """Get emission factor for the energy source (kg CO₂e per kWh)"""
        # In a real implementation, this would query the database
        emission_factors = {
            'electricity': 0.5,    # kg CO₂e per kWh (grid average)
            'natural_gas': 0.2,    # kg CO₂e per kWh
            'solar': 0.05,         # kg CO₂e per kWh (manufacturing & maintenance)
            'wind': 0.01,          # kg CO₂e per kWh
            'diesel': 0.27,        # kg CO₂e per kWh
            'propane': 0.24,       # kg CO₂e per kWh
        }
        
        energy_source = self.parameters['energy_source']
        return emission_factors.get(energy_source, 0.5)  # Default to grid average
    
    def get_annual_energy_consumption(self) -> float:
        """Get annual energy consumption in kWh"""
        return self.parameters['annual_consumption_kwh']
    
    def get_efficiency_rating(self) -> str:
        """Get efficiency rating as a descriptive string"""
        efficiency = self.parameters['efficiency']
        if efficiency >= 0.9:
            return "High Efficiency"
        elif efficiency >= 0.7:
            return "Medium Efficiency"
        else:
            return "Low Efficiency"