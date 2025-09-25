from abc import ABC, abstractmethod
from typing import Dict, Any

class Component(ABC):
    """Abstract base class for all building components"""
    
    def __init__(self, name: str, component_type: str):
        self.name = name
        self.component_type = component_type
        self.parameters: Dict[str, Any] = {}
    
    @abstractmethod
    def calculate_emissions(self, quantity: float = 1.0) -> float:
        """Calculate emissions for this component"""
        pass
    
    def update_parameters(self, new_parameters: Dict[str, Any]) -> None:
        """Update component parameters"""
        self.parameters.update(new_parameters)
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get a specific parameter value"""
        return self.parameters.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary for serialization"""
        return {
            'name': self.name,
            'component_type': self.component_type,
            'parameters': self.parameters
        }
    
    def __str__(self) -> str:
        return f"{self.component_type.capitalize()}Component({self.name})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', parameters={self.parameters})"