from typing import List, Optional
from .database import DatabaseHandler
from src.core.models import (
    BuildingComponentLink, 
    BuildingCreate, 
    BuildingResponse, 
    BuildingComponentResponse, 
    BuildingComponentUpdate, 
    BuildingComponentUpdateResponse, 
    ComponentResponse, 
    ComponentCreate, 
    ComponentUpdate, 
    EmissionFactorCreate, 
    EmissionFactorResponse, 
    EmissionFactorUpdate
)
from datetime import datetime

class BaseRepository:
    def __init__(self, table_name: str):
        self.db = DatabaseHandler()
        self.table_name = table_name

class ComponentRepository(BaseRepository):
    def __init__(self):
        super().__init__('components')
    
    def create(self, component_data: ComponentCreate) -> ComponentResponse:
        return self.db.insert(self.table_name, component_data)
    
    def get_by_id(self, component_id: str) -> Optional[ComponentResponse]:
        results = self.db.select(self.table_name, {'id': component_id})
        return results[0] if results else None
    
    def get_by_type(self, component_type: str) -> List[ComponentResponse]:
        return self.db.select(self.table_name, {'component_type': component_type})
    
    def get_all(self) -> List[ComponentResponse]:
        return self.db.select(self.table_name)

    def update(self, component_id: str, updates: ComponentUpdate) -> ComponentResponse:
        return self.db.update(self.table_name, component_id, updates)
    
    def delete(self, component_id: str) -> dict:
        return self.db.delete(self.table_name, component_id)

class BuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('buildings')
        self.components_by_building_repo = ComponentsByBuildingRepository()
    
    def create(self, building_data: BuildingCreate) -> BuildingResponse:
        building_data.pop('components_list', None)
        return self.db.insert(self.table_name, building_data)
    
    def get_by_id(self, building_id: str) -> Optional[BuildingResponse]:
        building = self.db.select(self.table_name, {'id': building_id})
        if not building:
            return None
        
        building = building[0]
        return building
    
    def get_with_components(self, building_id: str) -> Optional[BuildingResponse]:
        """Get building with all its components"""
        building = self.db.select(self.table_name, {'id': building_id})
        if not building:
            return None
        
        building = building[0]
        components = self.components_by_building_repo.get_components_for_building(building_id)
        building['components'] = components
        
        return building

    def get_by_name(self, name: str) -> Optional[BuildingResponse]:
        building = self.db.select(self.table_name, {'name': name})
        if not building:
            return None
        
        building = building[0]
        return building
    
    def get_all(self) -> List[BuildingResponse]:
        return self.db.select(self.table_name)

class ComponentsByBuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('components_by_building')
    
    def add_component_to_building(self, building_id: str, component_id: str, quantity: int = 1) -> BuildingComponentResponse:
        """Add a component to a building"""
        return self.db.insert(self.table_name, {
            'building_id': building_id,
            'component_id': component_id,
            'quantity': quantity
        })

    def add_components_to_building(self, building_id: str, components: List[BuildingComponentLink]) -> List[BuildingComponentResponse]:
        """Add a component to a building"""
        return self.db.insert_many(self.table_name, [
            {
            'building_id': building_id,
            'component_id': component.component_id,
            'quantity': component.quantity
        } for component in components])
    
    def get_components_for_building(self, building_id: str) -> List[BuildingComponentResponse]:
        response = self.db.get().table(self.table_name).select('quantity, components(*)').eq('building_id', building_id).execute()
        return response.data if response.data else []
    
    def remove_component_from_building(self, building_id: str, component_id: str) -> bool:
        """Remove a component from a building"""
        result = self.db.delete(self.table_name, {
            'building_id': building_id,
            'component_id': component_id
        })
        return bool(result)
    
    def update_component_quantity(self, building_id: str, component_id: str, quantity: int) -> BuildingComponentUpdateResponse:
        """Update the quantity of a component in a building"""
        join_record = self.db.select(self.table_name, {
            'building_id': building_id,
            'component_id': component_id
        })
        
        if not join_record:
            raise ValueError("Component not found in building")
        
        return self.db.update(self.table_name, join_record[0]['id'], {'quantity': quantity})

class EmissionFactorRepository(BaseRepository):
    def __init__(self):
        super().__init__('emission_factors')
    
    def create(self, factor_data: EmissionFactorCreate) -> EmissionFactorResponse:
        """Create a new emission factor"""
        # Add timestamp
        factor_data['created_at'] = datetime.now().isoformat()
        factor_data['updated_at'] = factor_data['created_at']
        
        return self.db.insert(self.table_name, factor_data)
    
    def get_by_id(self, factor_id: str) -> Optional[EmissionFactorResponse]:
        """Get emission factor by ID"""
        results = self.db.select(self.table_name, {'id': factor_id})
        return results[0] if results else None
    
    def get_by_category(self, category: str) -> List[EmissionFactorResponse]:
        """Get emission factors by category"""
        return self.db.select(self.table_name, {'category': category})
    
    def get_all(self) -> List[EmissionFactorResponse]:
        """Get all emission factors"""
        return self.db.select(self.table_name)
    
    def update(self, factor_id: str, updates: EmissionFactorUpdate) -> EmissionFactorResponse:
        """Update an emission factor"""
        updates['updated_at'] = datetime.now().isoformat()
        return self.db.update(self.table_name, factor_id, updates)
    
    def delete(self, factor_id: str) -> dict:
        """Delete an emission factor"""
        return self.db.delete(self.table_name, factor_id)
    
    def search(self, category: str = None, name_contains: str = None, 
               min_factor: float = None, max_factor: float = None) -> List[EmissionFactorResponse]:
        """Search emission factors with filters"""
        all_factors = self.get_all()
        results = []
        
        for factor in all_factors:
            # Filter by category
            if category and factor['category'] != category:
                continue
            
            # Filter by name contains
            if name_contains and name_contains.lower() not in factor['name'].lower():
                continue
            
            # Filter by min factor
            if min_factor is not None and factor['emission_factor'] < min_factor:
                continue
            
            # Filter by max factor
            if max_factor is not None and factor['emission_factor'] > max_factor:
                continue
            
            results.append(factor)
        
        return results
