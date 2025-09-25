from src.data.repositories import EmissionFactorRepository
from typing import List, Dict, Any, Optional, List
from src.core.models import (
    EmissionFactorCategory, 
    EmissionFactorCreate, 
    EmissionFactorResponse, 
    EmissionFactorUpdate
)

class EmissionFactorService:
    def __init__(self):
        self.emission_factor_repo = EmissionFactorRepository()
    
    def create_emission_factor(self, emission_factor_data: EmissionFactorCreate) -> EmissionFactorResponse:
        """Create a new emission factor"""
        # Validate that emission factor is positive
        if emission_factor_data.get('emission_factor', 0) < 0:
            raise ValueError("Emission factor must be positive")
        
        return self.emission_factor_repo.create(emission_factor_data)
    
    def get_emission_factor(self, factor_id: str) -> Optional[EmissionFactorResponse]:
        """Get a specific emission factor by ID"""
        return self.emission_factor_repo.get_by_id(factor_id)
    
    def get_all_emission_factors(self) -> List[EmissionFactorResponse]:
        """Get all emission factors"""
        return self.emission_factor_repo.get_all()
    
    def get_emission_factors_by_name_and_category(self, name: str, category: EmissionFactorCategory) -> List[EmissionFactorResponse]:
        """Get emission factors by category and source"""
        return self.emission_factor_repo.get_by_name_and_category(name, category.value)
    
    def get_emission_factors_by_category(self, category: EmissionFactorCategory) -> List[EmissionFactorResponse]:
        """Get emission factors by category"""
        return self.emission_factor_repo.get_by_category(category.value)
    
    def update_emission_factor(self, factor_id: str, updates: EmissionFactorUpdate) -> EmissionFactorResponse:
        """Update an emission factor"""
        factor = self.emission_factor_repo.get_by_id(factor_id)
        if not factor:
            raise ValueError(f"Emission factor {factor_id} not found")
        
        # Validate emission factor if it's being updated
        if 'emission_factor' in updates and updates['emission_factor'] < 0:
            raise ValueError("Emission factor must be positive")
        
        return self.emission_factor_repo.update(factor_id, updates)
    
    def delete_emission_factor(self, factor_id: str) -> dict:
        """Delete an emission factor"""
        factor = self.emission_factor_repo.get_by_id(factor_id)
        if not factor:
            raise ValueError(f"Emission factor {factor_id} not found")
        
        result = self.emission_factor_repo.delete(factor_id)
        return result
    
    def bulk_import_factors(self, factors_data: List[EmissionFactorCreate]) -> Dict[str, Any]:
        """Import multiple emission factors at once"""
        successful = 0
        failed = 0
        errors = []
        
        for factor_data in factors_data:
            try:
                self.create_emission_factor(factor_data)
                successful += 1
            except Exception as e:
                failed += 1
                errors.append({
                    'factor_data': factor_data,
                    'error': str(e)
                })
        
        return {
            'total_processed': len(factors_data),
            'successful': successful,
            'failed': failed,
            'errors': errors
        }