from fastapi import APIRouter, HTTPException
from typing import List
from src.core.models import (
    EmissionFactorCreate,
    EmissionFactorUpdate,
    EmissionFactorCategory
)
from src.services.emmission_service import EmissionFactorService

router = APIRouter(prefix="/emission_factors", tags=["emission_factors"])
emission_factor_service = EmissionFactorService()

@router.post("/", response_model=dict)
async def create_emission_factor(factor: EmissionFactorCreate):
    """Create a new emission factor"""
    try:
        result = emission_factor_service.create_emission_factor(factor.dict())
        return {
            "message": "Emission factor created successfully",
            "factor_id": result['id'],
            "factor": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create emission factor: {str(e)}")

@router.get("/", response_model=dict)
async def get_emission_factors():
    """Get emission factors with optional filtering"""
    try:
        factors = emission_factor_service.get_all_emission_factors()
        
        return {
            "count": len(factors),
            "emission_factors": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emission factors: {str(e)}")

@router.get("/{factor_id}", response_model=dict)
async def get_emission_factor(factor_id: str):
    """Get a specific emission factor by ID"""
    try:
        factor = emission_factor_service.get_emission_factor(factor_id)
        if not factor:
            raise HTTPException(status_code=404, detail=f"Emission factor {factor_id} not found")
        
        return {"emission_factor": factor}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emission factor: {str(e)}")

@router.get("/category/{category}", response_model=dict)
async def get_emission_factors_by_category(category: EmissionFactorCategory):
    """Get all emission factors for a specific category"""
    try:
        factors = emission_factor_service.get_emission_factors_by_category(category)
        return {
            "category": category.value,
            "count": len(factors),
            "emission_factors": factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emission factors: {str(e)}")

@router.put("/{factor_id}", response_model=dict)
async def update_emission_factor(factor_id: str, updates: EmissionFactorUpdate):
    """Update an emission factor"""
    try:
        # Remove None values from updates
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        result = emission_factor_service.update_emission_factor(factor_id, update_data)
        return {
            "message": "Emission factor updated successfully",
            "factor": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update emission factor: {str(e)}")

@router.delete("/{factor_id}", response_model=dict)
async def delete_emission_factor(factor_id: str):
    """Delete an emission factor"""
    try:
        success = emission_factor_service.delete_emission_factor(factor_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Emission factor {factor_id} not found")
        
        return {"message": "Emission factor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete emission factor: {str(e)}")

@router.post("/bulk-import", response_model=dict)
async def bulk_import_emission_factors(factors: List[EmissionFactorCreate]):
    """Import multiple emission factors at once"""
    try:
        factors_data = [factor.dict() for factor in factors]
        result = emission_factor_service.bulk_import_factors(factors_data)
        
        return {
            "message": "Bulk import completed",
            "results": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import emission factors: {str(e)}")

@router.get("/categories/available", response_model=dict)
async def get_available_categories():
    """Get all available emission factor categories"""
    try:
        categories = [{"value": cat.value, "label": cat.value.capitalize()} for cat in EmissionFactorCategory]
        return {
            "categories": categories,
            "count": len(categories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")
