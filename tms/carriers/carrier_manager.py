"""
Carrier Management Module for TMS
Handles carrier information, rate calculation, and carrier selection
"""

from typing import Dict, List, Optional
from datetime import datetime


class Carrier:
    """Represents a shipping carrier"""
    
    def __init__(self, carrier_id: str, name: str, service_type: str):
        self.carrier_id = carrier_id
        self.name = name
        self.service_type = service_type  # e.g., "standard", "express", "overnight"
        self.active = True
        self.base_rate = 0.0
        self.per_kg_rate = 0.0
        self.transit_days = 0
        self.api_endpoint: Optional[str] = None
        self.api_key: Optional[str] = None
        self.supported_countries: List[str] = []
        
    def calculate_rate(self, weight: float, distance: float) -> float:
        """Calculate shipping rate based on weight and distance"""
        return self.base_rate + (weight * self.per_kg_rate) + (distance * 0.01)
    
    def to_dict(self) -> Dict:
        return {
            'carrier_id': self.carrier_id,
            'name': self.name,
            'service_type': self.service_type,
            'active': self.active,
            'base_rate': self.base_rate,
            'per_kg_rate': self.per_kg_rate,
            'transit_days': self.transit_days,
            'supported_countries': self.supported_countries
        }


class CarrierManager:
    """Manages carrier operations and selection"""
    
    def __init__(self):
        self.carriers: Dict[str, Carrier] = {}
        
    def add_carrier(self, carrier: Carrier) -> bool:
        """Add a carrier to the system"""
        if carrier.carrier_id in self.carriers:
            return False
        self.carriers[carrier.carrier_id] = carrier
        return True
    
    def get_carrier(self, carrier_id: str) -> Optional[Carrier]:
        """Get a carrier by ID"""
        return self.carriers.get(carrier_id)
    
    def get_active_carriers(self) -> List[Carrier]:
        """Get all active carriers"""
        return [c for c in self.carriers.values() if c.active]
    
    def deactivate_carrier(self, carrier_id: str) -> bool:
        """Deactivate a carrier"""
        carrier = self.get_carrier(carrier_id)
        if carrier:
            carrier.active = False
            return True
        return False
    
    def activate_carrier(self, carrier_id: str) -> bool:
        """Activate a carrier"""
        carrier = self.get_carrier(carrier_id)
        if carrier:
            carrier.active = True
            return True
        return False
    
    def get_best_carrier(self, weight: float, distance: float, 
                        service_type: Optional[str] = None) -> Optional[Carrier]:
        """Select the best carrier based on criteria"""
        eligible_carriers = [c for c in self.get_active_carriers()
                           if service_type is None or c.service_type == service_type]
        
        if not eligible_carriers:
            return None
        
        # Select carrier with lowest rate
        best_carrier = min(eligible_carriers, 
                          key=lambda c: c.calculate_rate(weight, distance))
        return best_carrier
    
    def get_rate_quotes(self, weight: float, distance: float) -> List[Dict]:
        """Get rate quotes from all active carriers"""
        quotes = []
        for carrier in self.get_active_carriers():
            rate = carrier.calculate_rate(weight, distance)
            quotes.append({
                'carrier_id': carrier.carrier_id,
                'carrier_name': carrier.name,
                'service_type': carrier.service_type,
                'rate': rate,
                'transit_days': carrier.transit_days
            })
        return sorted(quotes, key=lambda x: x['rate'])
