from .base import Component
from typing import Dict, Any
from pydantic import BaseModel
from src.services.emission_factor_service import EmissionFactorService
from src.core.models import EmissionFactorCategory

class WaterMetadata(BaseModel):
    annual_consumption_liters: float
    water_treatment_factor: float
    treatment_type: str

class WaterComponent(Component):
    """Component for water consumption and treatment systems"""
    
    def __init__(self, name: str, metadata: WaterMetadata, **kwargs):
        super().__init__(name, "water")
        self.metadata = {
            'annual_consumption_liters': metadata['annual_consumption_liters'],
            'water_treatment_factor': metadata['water_treatment_factor'],
            'treatment_type': metadata['treatment_type'],
            **kwargs
        }
        self.emission_factor_service = EmissionFactorService()

    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate emissions for water consumption and treatment"""
        try:
            # Get water treatment emission factor (kg CO₂e per liter)
            emission_factor = self._get_water_emission_factor()
            
            # Calculate effective consumption considering treatment factor
            effective_consumption = (self.metadata['annual_consumption_liters'] * 
                                   self.metadata['water_treatment_factor'])
            
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
        factors = self.emission_factor_service.get_emission_factors_by_name_and_category(self.metadata['treatment_type'], EmissionFactorCategory.WATER)
        if not factors:
            raise ValueError(f"No emission factors found for {self.metadata['treatment_type']}")
        if len(factors) > 1:
            raise ValueError(f"Multiple emission factors found for {self.metadata['treatment_type']}")
        return float(factors[0]['emission_factor'])
    
    def _calculate_pumping_emissions(self) -> float:
        """Calculate emissions from water pumping"""
        pumping_energy_kwh = self.metadata.get('pumping_energy_kwh', 0)
        if pumping_energy_kwh <= 0:
            return 0
        
        # Electricity emission factor (kg CO₂e per kWh)
        electricity_factor = 0.5
        return pumping_energy_kwh * electricity_factor
    
    def get_daily_consumption(self) -> float:
        """Get daily water consumption in liters"""
        return self.metadata['annual_consumption_liters'] / 365
    
    def get_water_savings_potential(self, efficiency_improvement: float = 0.2) -> float:
        """Calculate potential water savings with efficiency improvements"""
        current_consumption = self.metadata['annual_consumption_liters']
        return current_consumption * efficiency_improvement