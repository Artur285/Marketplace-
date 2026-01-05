"""
Shipment Tracking Module for TMS
Handles shipment creation, tracking, and status updates
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ShipmentStatus(Enum):
    """Shipment status enumeration"""
    CREATED = "created"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETURNED = "returned"


class TrackingEvent:
    """Represents a tracking event in the shipment journey"""
    
    def __init__(self, status: ShipmentStatus, location: str, 
                 description: str, timestamp: datetime = None):
        self.status = status
        self.location = location
        self.description = description
        self.timestamp = timestamp or datetime.now()
        
    def to_dict(self) -> Dict:
        return {
            'status': self.status.value,
            'location': self.location,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }


class Shipment:
    """Represents a shipment"""
    
    def __init__(self, shipment_id: str, order_id: str, carrier_id: str,
                 origin: Dict, destination: Dict):
        self.shipment_id = shipment_id
        self.order_id = order_id
        self.carrier_id = carrier_id
        self.origin = origin
        self.destination = destination
        self.tracking_number: Optional[str] = None
        self.status = ShipmentStatus.CREATED
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.estimated_delivery: Optional[datetime] = None
        self.actual_delivery: Optional[datetime] = None
        self.tracking_events: List[TrackingEvent] = []
        self.weight: Optional[float] = None
        self.dimensions: Optional[Dict] = None
        self.cost: Optional[float] = None
        
    def add_tracking_event(self, event: TrackingEvent):
        """Add a tracking event"""
        self.tracking_events.append(event)
        self.status = event.status
        self.updated_at = datetime.now()
        
        if event.status == ShipmentStatus.DELIVERED:
            self.actual_delivery = event.timestamp
            
    def to_dict(self) -> Dict:
        return {
            'shipment_id': self.shipment_id,
            'order_id': self.order_id,
            'carrier_id': self.carrier_id,
            'tracking_number': self.tracking_number,
            'status': self.status.value,
            'origin': self.origin,
            'destination': self.destination,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'actual_delivery': self.actual_delivery.isoformat() if self.actual_delivery else None,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'cost': self.cost,
            'tracking_events': [event.to_dict() for event in self.tracking_events]
        }


class ShipmentTracker:
    """Manages shipment tracking operations"""
    
    def __init__(self):
        self.shipments: Dict[str, Shipment] = {}
        self.tracking_index: Dict[str, str] = {}  # tracking_number -> shipment_id
        
    def create_shipment(self, shipment: Shipment) -> bool:
        """Create a new shipment"""
        if shipment.shipment_id in self.shipments:
            return False
        
        self.shipments[shipment.shipment_id] = shipment
        
        # Add initial tracking event
        event = TrackingEvent(
            ShipmentStatus.CREATED,
            shipment.origin.get('city', 'Unknown'),
            "Shipment created"
        )
        shipment.add_tracking_event(event)
        
        return True
    
    def get_shipment(self, shipment_id: str) -> Optional[Shipment]:
        """Get a shipment by ID"""
        return self.shipments.get(shipment_id)
    
    def get_shipment_by_tracking(self, tracking_number: str) -> Optional[Shipment]:
        """Get a shipment by tracking number"""
        shipment_id = self.tracking_index.get(tracking_number)
        return self.shipments.get(shipment_id) if shipment_id else None
    
    def assign_tracking_number(self, shipment_id: str, tracking_number: str) -> bool:
        """Assign a tracking number to a shipment"""
        shipment = self.get_shipment(shipment_id)
        if shipment:
            shipment.tracking_number = tracking_number
            self.tracking_index[tracking_number] = shipment_id
            shipment.updated_at = datetime.now()
            return True
        return False
    
    def update_status(self, shipment_id: str, status: ShipmentStatus,
                     location: str, description: str) -> bool:
        """Update shipment status"""
        shipment = self.get_shipment(shipment_id)
        if shipment:
            event = TrackingEvent(status, location, description)
            shipment.add_tracking_event(event)
            return True
        return False
    
    def get_shipments_by_order(self, order_id: str) -> List[Shipment]:
        """Get all shipments for an order"""
        return [s for s in self.shipments.values() if s.order_id == order_id]
    
    def get_shipments_by_carrier(self, carrier_id: str) -> List[Shipment]:
        """Get all shipments for a carrier"""
        return [s for s in self.shipments.values() if s.carrier_id == carrier_id]
    
    def get_active_shipments(self) -> List[Shipment]:
        """Get all active (in-transit) shipments"""
        active_statuses = {
            ShipmentStatus.CREATED,
            ShipmentStatus.PICKED_UP,
            ShipmentStatus.IN_TRANSIT,
            ShipmentStatus.OUT_FOR_DELIVERY
        }
        return [s for s in self.shipments.values() if s.status in active_statuses]
