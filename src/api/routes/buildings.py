from fastapi import APIRouter, HTTPException, Query
from src.core.models import BuildingComponentUpdate, BuildingCreate, BuildingResponse, EmissionCalculationRequest
from src.services.building_service import BuildingService
from typing import Optional

router = APIRouter(prefix="/buildings", tags=["buildings"])
building_service = BuildingService()

@router.post("/", response_model=dict)
async def create_building(building: BuildingCreate):
    """Create a new building digital twin"""
    try:
        result = building_service.create_building(
            name=building.name,
            location=building.location,
            component_ids_with_quantities=building.components
        )
        return {"message": "Building created", "building_id": result['id']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
async def get_buildings(
    name: Optional[str] = Query(None, description="Filter by building name"),
):
    """Get all components, with optional filtering"""
    try:
        if name:
            components = building_service.get_buildings_by_name(name)
        else:
            buildings = building_service.get_all_buildings()
        
        return {
            "count": len(buildings),
            "buildings": buildings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve buildings: {str(e)}")

@router.get("/{building_id}", response_model=dict)
async def get_building(building_id: str):
    """Get a specific building by ID"""
    try:
        building = building_service.get_building(building_id)
        if not building:
            raise HTTPException(status_code=404, detail=f"Building {building_id} not found")
        
        return {"building": building}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve building: {str(e)}")

@router.post("/{building_id}/components/{component_id}", response_model=dict)
async def add_component_to_building(building_id: str, component_id: str, quantity: int = 1):
    """Add a component to a building"""
    try:
        result = building_service.add_component_to_building(building_id, component_id, quantity)
        return {"message": "Component added to building", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{building_id}/components", response_model=dict)
async def get_building_components(building_id: str):
    """Get all components for a building"""
    try:
        building_data = building_service.get_with_components(building_id)
        return {
            "building_id": building_id,
            "components": building_data.get('components', []) if building_data else []
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{building_id}/components/{component_id}", response_model=dict)
async def update_component_quantity(building_id: str, component_id: str, update: BuildingComponentUpdate):
    """Update the quantity of a component in a building"""
    try:
        result = building_service.update_component_quantity(building_id, component_id, update.quantity)
        return {"message": "Component quantity updated", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{building_id}/calculate", response_model=dict)
async def calculate_emissions(building_id: str):
    """Calculate emissions for a building with optional real-time modifications"""
    try:
        results = building_service.calculate_building_emissions(
            building_id, 
            {}
        )
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))