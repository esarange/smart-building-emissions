from fastapi import APIRouter, HTTPException
from src.core.models import BuildingCreate, BuildingResponse, EmissionCalculationRequest
from src.services.building_service import BuildingService

router = APIRouter(prefix="/buildings", tags=["buildings"])
building_service = BuildingService()

@router.post("/", response_model=dict)
async def create_building(building: BuildingCreate):
    """Create a new building digital twin"""
    try:
        result = building_service.create_building(
            name=building.name,
            location=building.location,
            component_ids=building.component_ids
        )
        return {"message": "Building created", "building_id": result['id']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{building_id}/components/{component_id}")
async def add_component_to_building(building_id: int, component_id: int, quantity: int = 1):
    """Add a component to a building"""
    try:
        result = building_service.add_component_to_building(building_id, component_id, quantity)
        return {"message": "Component added to building", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{building_id}/components")
async def get_building_components(building_id: int):
    """Get all components for a building"""
    try:
        building_data = building_service.building_repo.get_with_components(building_id)
        return {
            "building_id": building_id,
            "components": building_data.get('components', []) if building_data else []
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{building_id}/calculate", response_model=dict)
async def calculate_emissions(building_id: int, request: EmissionCalculationRequest):
    """Calculate emissions for a building with optional real-time modifications"""
    try:
        results = building_service.calculate_building_emissions(
            building_id, 
            request.modifications
        )
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))