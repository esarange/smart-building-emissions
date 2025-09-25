from .base import Component
from typing import Dict, Any
from src.services.emission_factor_service import EmissionFactorService
from src.core.models import EmissionFactorCategory
from pydantic import BaseModel

class EnergyMetadata(BaseModel):
    energy_source: str
    efficiency: float
    annual_consumption_kwh: float

class EnergyComponent(Component):
    """Component for energy consumption systems (HVAC, lighting, etc.)"""
    
    def __init__(self, name: str, metadata: EnergyMetadata, **kwargs):
        super().__init__(name, "energy")
        self.metadata = {
            'energy_source': metadata['energy_source'],
            'efficiency': metadata['efficiency'],
            'annual_consumption_kwh': metadata['annual_consumption_kwh'],
            **kwargs
        }
        self.emission_factor_service = EmissionFactorService()
    
    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate operational emissions for energy consumption"""
        try:
            emission_factor = self._get_energy_emission_factor()

            # Calculate effective energy consumption considering efficiency
            effective_consumption = (float(self.metadata['annual_consumption_kwh']) / 
                                   float(self.metadata['efficiency']))

            # Calculate emissions: energy consumption * emission factor * quantity
            emissions = float(effective_consumption) * float(emission_factor) * quantity

            # Add embodied emissions if specified
            embodied_emissions = self.metadata.get('embodied_emissions', 0)
            emissions += float(embodied_emissions) * quantity
            return round(emissions, 2)
            
        except KeyError as e:
            raise ValueError(f"Missing required parameter for energy calculation: {e}")
        except ZeroDivisionError:
            raise ValueError("Efficiency cannot be zero")
    
    def _get_energy_emission_factor(self) -> float:
        """Get emission factor for the energy source (kg CO₂e per kWh)"""
        factors = self.emission_factor_service.get_emission_factors_by_name_and_category(self.metadata['energy_source'], EmissionFactorCategory.ENERGY)
        if not factors:
            raise ValueError(f"No emission factors found for {self.metadata['energy_source']}")
        if len(factors) > 1:
            raise ValueError(f"Multiple emission factors found for {self.metadata['energy_source']}")
        return float(factors[0]['emission_factor'])
    
    def get_annual_energy_consumption(self) -> float:
        """Get annual energy consumption in kWh"""
        return self.metadata['annual_consumption_kwh']
    
    def get_efficiency_rating(self) -> str:
        """Get efficiency rating as a descriptive string"""
        efficiency = self.metadata['efficiency']
        if efficiency >= 0.9:
            return "High Efficiency"
        elif efficiency >= 0.7:
            return "Medium Efficiency"
        else:
            return "Low Efficiency"