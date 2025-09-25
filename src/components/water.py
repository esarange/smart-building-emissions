from .base import Component
from typing import Dict, Any

class WaterComponent(Component):
    """Component for water consumption and treatment systems"""
    
    def __init__(self, name: str, annual_consumption_liters: float, 
                 water_treatment_factor: float = 1.0, **kwargs):
        super().__init__(name, "water")
        self.parameters = {
            'annual_consumption_liters': annual_consumption_liters,
            'water_treatment_factor': water_treatment_factor,
            **kwargs
        }
    
    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate emissions for water consumption and treatment"""
        try:
            # Get water treatment emission factor (kg CO₂e per liter)
            emission_factor = self._get_water_emission_factor()
            
            # Calculate effective consumption considering treatment factor
            effective_consumption = (self.parameters['annual_consumption_liters'] * 
                                   self.parameters['water_treatment_factor'])
            
            # Calculate emissions: water consumption * emission factor * quantity
            emissions = effective_consumption * emission_factor * quantity
            
            # Add pumping energy emissions if specified
            pumping_emissions = self._calculate_pumping_emissions()
            emissions += pumping_emissions * quantity
            
            return round(emissions, 2)
            
        except KeyError as e:
            raise ValueError(f"Missing required parameter for water calculation: {e}")
    
    def _get_water_emission_factor(self) -> float:
        """Get emission factor for water treatment (kg CO₂e per liter)"""
        # Emission factors for water treatment processes
        treatment_factors = {
            'standard': 0.0005,    # kg CO₂e per liter (standard treatment)
            'advanced': 0.001,     # kg CO₂e per liter (advanced treatment)
            'recycling': 0.0008,   # kg CO₂e per liter (water recycling)
            'desalination': 0.003, # kg CO₂e per liter (desalination)
        }
        
        treatment_type = self.parameters.get('treatment_type', 'standard')
        return treatment_factors.get(treatment_type, 0.0005)
    
    def _calculate_pumping_emissions(self) -> float:
        """Calculate emissions from water pumping"""
        pumping_energy_kwh = self.parameters.get('pumping_energy_kwh', 0)
        if pumping_energy_kwh <= 0:
            return 0
        
        # Electricity emission factor (kg CO₂e per kWh)
        electricity_factor = 0.5
        return pumping_energy_kwh * electricity_factor
    
    def get_daily_consumption(self) -> float:
        """Get daily water consumption in liters"""
        return self.parameters['annual_consumption_liters'] / 365
    
    def get_water_savings_potential(self, efficiency_improvement: float = 0.2) -> float:
        """Calculate potential water savings with efficiency improvements"""
        current_consumption = self.parameters['annual_consumption_liters']
        return current_consumption * efficiency_improvement