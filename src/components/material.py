from .base import Component
from typing import Dict, Any

class MaterialComponent(Component):
    """Component for building materials (steel, concrete, glass, etc.)"""
    
    def __init__(self, name: str, material_name: str, density_kg_m3: float = None, 
                 **kwargs):
        super().__init__(name, "material")
        self.parameters = {
            'material_name': material_name,
            'density_kg_m3': density_kg_m3,
            **kwargs
        }
    
    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate embodied emissions for material quantity"""
        try:
            # Get emission factor for the material (kg CO₂e per kg of material)
            emission_factor = self._get_material_emission_factor()
            
            # Calculate emissions: quantity * emission factor
            # Quantity could be in kg, or if density is provided, convert from m³ to kg
            if self.parameters.get('density_kg_m3') and self.parameters.get('volume_m3'):
                # Convert volume to mass using density
                mass_kg = self.parameters['volume_m3'] * self.parameters['density_kg_m3']
                emissions = mass_kg * emission_factor
            else:
                # Assume quantity is already in kg
                emissions = quantity * emission_factor
            
            # Apply recycling rate if specified
            recycling_rate = self.parameters.get('recycling_rate', 0)
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
        # In a real implementation, this would query the database
        emission_factors = {
            'concrete': 0.12,      # kg CO₂e per kg
            'steel': 1.85,         # kg CO₂e per kg
            'glass': 0.85,         # kg CO₂e per kg
            'wood': 0.45,          # kg CO₂e per kg (varies by type)
            'aluminum': 8.24,      # kg CO₂e per kg
            'insulation': 2.1,     # kg CO₂e per kg
            'brick': 0.22,         # kg CO₂e per kg
        }
        
        material_name = self.parameters['material_name']
        return emission_factors.get(material_name, 1.0)  # Default factor
    
    def _calculate_transport_emissions(self, quantity: float) -> float:
        """Calculate transport emissions if distance is specified"""
        distance_km = self.parameters.get('transport_distance_km', 0)
        if distance_km <= 0:
            return 0
        
        # Transport emission factor (kg CO₂e per kg-km)
        transport_factor = 0.0001  # Typical truck transport factor
        
        return quantity * distance_km * transport_factor
    
    def get_material_density(self) -> float:
        """Get material density in kg/m³"""
        return self.parameters.get('density_kg_m3', 0)
    
    def calculate_volume_from_mass(self, mass_kg: float) -> float:
        """Calculate volume from mass using density"""
        density = self.get_material_density()
        if density > 0:
            return mass_kg / density
        return 0