from fastapi import APIRouter, HTTPException
from src.core.models import BuildingCreate, BuildingResponse, EmissionCalculationRequest
from src.services.building_service import BuildingService

router = APIRouter(prefix="/buildings", tags=["buildings"])
building_service = BuildingService()

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
