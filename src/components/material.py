from .base import Component
from typing import Dict, Any
from pydantic import BaseModel
from src.services.emission_factor_service import EmissionFactorService
from src.core.models import EmissionFactorCategory

class MaterialMetadata(BaseModel):
    material_name: str
    density_kg_m3: float
    volume_m3: float
    # recycling_rate: float
    # transport_distance_km: float

class MaterialComponent(Component):
    """Component for building materials (steel, concrete, glass, etc.)"""
    
    def __init__(self, name: str, metadata: MaterialMetadata, **kwargs):
        super().__init__(name, "material")
        self.metadata = {
            'material_name': metadata['material_name'],
            'density_kg_m3': metadata['density_kg_m3'],
            'volume_m3': metadata['volume_m3'],
            # 'recycling_rate': metadata['recycling_rate'],
            # 'transport_distance_km': metadata['transport_distance_km'],
            **kwargs
        }
        self.emission_factor_service = EmissionFactorService()

    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate embodied emissions for material quantity"""
        try:
            # Get emission factor for the material (kg CO₂e per kg of material)
            emission_factor = self._get_material_emission_factor()
            
            # Calculate emissions: quantity * emission factor
            # Quantity could be in kg, or if density is provided, convert from m³ to kg
            if self.metadata.get('density_kg_m3') and self.metadata.get('volume_m3'):
                # Convert volume to mass using density
                mass_kg = self.metadata['volume_m3'] * self.metadata['density_kg_m3']
                emissions = mass_kg * emission_factor
            else:
                # Assume quantity is already in kg
                emissions = quantity * emission_factor
            
            # Apply recycling rate if specified
            recycling_rate = self.metadata.get('recycling_rate', 0)
            if recycling_rate > 0:
                # Reduce emissions based on recycling percentage
                emissions *= (1 - recycling_rate / 100)
            
            # Add transport emissions if distance is specified
            transport_emissions = self._calculate_transport_emissions(quantity)
            emissions += transport_emissions
            
            return round(emissions, 2)
            
        except KeyError as e:
            raise ValueError(f"Missing required parameter for material calculation: {e}")
    
    def _get_material_emission_factor(self) -> float:
        """Get emission factor for the material (kg CO₂e per kg)"""
        factors = self.emission_factor_service.get_emission_factors_by_name_and_category(self.metadata['material_name'], EmissionFactorCategory.MATERIAL)
        if not factors:
            raise ValueError(f"No emission factors found for {self.metadata['material_name']}")
        if len(factors) > 1:
            raise ValueError(f"Multiple emission factors found for {self.metadata['material_name']}")
        return float(factors[0]['emission_factor'])
    
    # TODO: Implement transport emissions
    def _calculate_transport_emissions(self, quantity: float) -> float:
        """Calculate transport emissions if distance is specified"""
        distance_km = self.metadata.get('transport_distance_km', 0)
        if distance_km <= 0:
            return 0
        
        # Transport emission factor (kg CO₂e per kg-km)
        # TODO: Implement transport emission factor
        transport_factor = 0.0001  # Typical truck transport factor
        
        return quantity * distance_km * transport_factor
    
    def get_material_density(self) -> float:
        """Get material density in kg/m³"""
        return self.metadata.get('density_kg_m3', 0)
    
    def calculate_volume_from_mass(self, mass_kg: float) -> float:
        """Calculate volume from mass using density"""
        density = self.get_material_density()
        if density > 0:
            return mass_kg / density
        return 0