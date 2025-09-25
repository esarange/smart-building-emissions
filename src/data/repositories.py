from typing import List, Optional
from .database import DatabaseHandler

class BaseRepository:
    def __init__(self, table_name: str):
        self.db = DatabaseHandler()
        self.table_name = table_name

class ComponentRepository(BaseRepository):
    def __init__(self):
        super().__init__('components')
    
    def create(self, component_data: dict) -> dict:
        return self.db.insert(self.table_name, component_data)
    
    def get_by_id(self, component_id: int) -> Optional[dict]:
        results = self.db.select(self.table_name, {'id': component_id})
        return results[0] if results else None
    
    def get_by_type(self, component_type: str) -> List[dict]:
        return self.db.select(self.table_name, {'component_type': component_type})
    
    def get_all(self) -> List[dict]:
        return self.db.select(self.table_name)

class BuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('buildings')
    
    def create(self, building_data: dict) -> dict:
        return self.db.insert(self.table_name, building_data)
    
    def get_with_components(self, building_id: int) -> Optional[dict]:
        building = self.db.select(self.table_name, {'id': building_id})
        if not building:
            return None
        
        building = building[0]
        return building

class ComponentsByBuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('components_by_building')
    
    def add_component_to_building(self, building_id: int, component_id: int, quantity: int = 1) -> dict:
        """Add a component to a building"""
        return self.db.insert(self.table_name, {
            'building_id': building_id,
            'component_id': component_id,
            'quantity': quantity
        })
    
    def get_components_for_building(self, building_id: int) -> List[dict]:
        """Get all components for a specific building with their details"""
        query = """
            SELECT c.*, cxb.quantity 
            FROM components_by_building cxb
            JOIN components c ON cxb.component_id = c.id
            WHERE cxb.building_id = $1
        """
        response = self.db.get().execute(query, [building_id])
        return response.data if response.data else []
    
    def remove_component_from_building(self, building_id: int, component_id: int) -> bool:
        """Remove a component from a building"""
        result = self.db.delete(self.table_name, {
            'building_id': building_id,
            'component_id': component_id
        })
        return bool(result)
    
    def update_component_quantity(self, building_id: int, component_id: int, quantity: int) -> dict:
        """Update the quantity of a component in a building"""
        join_record = self.db.select(self.table_name, {
            'building_id': building_id,
            'component_id': component_id
        })
        
        if not join_record:
            raise ValueError("Component not found in building")
        
        return self.db.update(self.table_name, join_record[0]['id'], {'quantity': quantity})

class BuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('buildings')
        self.components_by_building_repo = ComponentsByBuildingRepository()
    
    def create(self, building_data: dict) -> dict:
        """Create a new building"""
        building_data.pop('components_list', None)
        return self.db.insert(self.table_name, building_data)
    
    def get_with_components(self, building_id: int) -> Optional[dict]:
        """Get building with all its components"""
        building = self.db.select(self.table_name, {'id': building_id})
        if not building:
            return None
        
        building = building[0]
        components = self.components_by_building_repo.get_components_for_building(building_id)
        building['components'] = components
        
        return building
    
    def add_component(self, building_id: int, component_id: int, quantity: int = 1) -> dict:
        """Add a component to a building"""
        return self.components_by_building_repo.add_component_to_building(building_id, component_id, quantity)