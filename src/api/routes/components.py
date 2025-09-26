from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.core.models import (
    ComponentCreate, 
    ComponentResponse, 
    ComponentType,
    ComponentUpdate
)
from src.services.component_service import ComponentService

router = APIRouter(prefix="/components", tags=["components"])
component_service = ComponentService()

@router.post("/", response_model=dict)
async def create_component(component: ComponentCreate):
    """Create a new component definition"""
    try:
        result = component_service.create_component(
            name=component.name,
            component_type=component.component_type,
            metadata=component.metadata
        )
        return {
            "message": "Component created successfully",
            "component_id": result['id'],
            "component": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create component: {str(e)}")

@router.get("/", response_model=dict)
async def get_components(
    component_type: Optional[ComponentType] = Query(None, description="Filter by component type"),
):
    """Get all components, with optional filtering"""
    try:
        if component_type:
            components = component_service.get_components_by_type(component_type)
        else:
            components = component_service.get_all_components()
        
        return {
            "count": len(components),
            "components": components
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve components: {str(e)}")

@router.get("/{component_id}", response_model=dict)
async def get_component(component_id: str):
    """Get a specific component by ID"""
    try:
        component = component_service.get_component(component_id)
        if not component:
            raise HTTPException(status_code=404, detail=f"Component {component_id} not found")
        
        return {"component": component}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve component: {str(e)}")

@router.put("/{component_id}", response_model=dict)
async def update_component(component_id: str, updates: ComponentUpdate):
    """Update a component's properties"""
    try:
        result = component_service.update_component(component_id, updates.dict(exclude_unset=True))
        return {
            "message": "Component updated successfully",
            "component": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update component: {str(e)}")

@router.delete("/{component_id}", response_model=dict)
async def delete_component(component_id: str):
    """Delete a component"""
    try:
        success = component_service.delete_component(component_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Component {component_id} not found")
        
        return {"message": "Component deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete component: {str(e)}")

@router.post("/{component_id}/calculate", response_model=dict)
async def calculate_component_emissions(
    component_id: str, 
    quantity: int = Query(1, description="Quantity of the component to calculate emissions for")
):
    """Calculate emissions for a specific component"""
    try:
        result = component_service.calculate_component_emissions(component_id, quantity)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate emissions: {str(e)}")

@router.get("/templates/{component_type}", response_model=dict)
async def get_component_template(component_type: ComponentType):
    """Get a template of required parameters for a specific component type"""
    try:
        template = component_service.get_component_template(component_type)
        return {
            "component_type": component_type.value,
            "template": template
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get template: {str(e)}")

@router.get("/types/available", response_model=dict)
async def get_available_component_types():
    """Get all available component types"""
    try:
        types = [{"value": ct.value, "label": ct.value.capitalize()} for ct in ComponentType]
        return {
            "component_types": types,
            "count": len(types)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get component types: {str(e)}")

@router.post("/batch-calculate", response_model=dict)
async def calculate_batch_emissions(components: List[dict]):
    """Calculate emissions for multiple components at once"""
    try:
        results = []
        total_emissions = 0.0
        
        for component_data in components:
            component_id = component_data.get('component_id')
            quantity = component_data.get('quantity', 1)
            
            if not component_id:
                continue
            
            result = component_service.calculate_component_emissions(component_id, quantity)
            results.append(result)
            total_emissions += result['emissions']
        
        return {
            "total_emissions": total_emissions,
            "components": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate batch emissions: {str(e)}")