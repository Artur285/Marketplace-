"""
Webhook Handler Module
Handles incoming webhook events from suppliers
"""

from typing import Dict, List, Callable, Optional
from datetime import datetime
from enum import Enum


class WebhookEventType(Enum):
    """Types of webhook events"""
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_SHIPPED = "order.shipped"
    ORDER_DELIVERED = "order.delivered"
    ORDER_CANCELLED = "order.cancelled"
    INVENTORY_UPDATED = "inventory.updated"
    SHIPMENT_TRACKING = "shipment.tracking"
    PAYMENT_RECEIVED = "payment.received"


class WebhookEvent:
    """Represents a webhook event"""
    
    def __init__(self, event_type: WebhookEventType, supplier_id: str, 
                 payload: Dict, signature: Optional[str] = None):
        self.event_id = f"{supplier_id}_{datetime.now().timestamp()}"
        self.event_type = event_type
        self.supplier_id = supplier_id
        self.payload = payload
        self.signature = signature
        self.received_at = datetime.now()
        self.processed = False
        self.processed_at: Optional[datetime] = None
        
    def to_dict(self) -> Dict:
        return {
            'event_id': self.event_id,
            'event_type': self.event_type.value,
            'supplier_id': self.supplier_id,
            'payload': self.payload,
            'received_at': self.received_at.isoformat(),
            'processed': self.processed,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class WebhookHandler:
    """Handles webhook events from suppliers"""
    
    def __init__(self):
        self.events: List[WebhookEvent] = []
        self.handlers: Dict[WebhookEventType, List[Callable]] = {}
        self.supplier_secrets: Dict[str, str] = {}
        
    def register_handler(self, event_type: WebhookEventType, handler: Callable):
        """Register a handler for a specific event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        
    def register_supplier_secret(self, supplier_id: str, secret: str):
        """Register a webhook secret for signature verification"""
        self.supplier_secrets[supplier_id] = secret
        
    def verify_signature(self, supplier_id: str, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        secret = self.supplier_secrets.get(supplier_id)
        if not secret:
            return False
        
        # In production, implement proper HMAC signature verification
        # import hmac, hashlib
        # expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        # return hmac.compare_digest(signature, expected)
        
        return True
    
    def receive_event(self, event: WebhookEvent, verify_signature: bool = True) -> bool:
        """Receive and queue a webhook event"""
        if verify_signature and event.signature:
            import json
            payload_str = json.dumps(event.payload)
            if not self.verify_signature(event.supplier_id, payload_str, event.signature):
                return False
        
        self.events.append(event)
        return True
    
    def process_event(self, event: WebhookEvent) -> bool:
        """Process a webhook event"""
        if event.processed:
            return True
        
        handlers = self.handlers.get(event.event_type, [])
        if not handlers:
            return False
        
        success = True
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Error processing event {event.event_id}: {e}")
                success = False
        
        event.processed = True
        event.processed_at = datetime.now()
        return success
    
    def process_pending_events(self) -> int:
        """Process all pending events"""
        processed_count = 0
        for event in self.events:
            if not event.processed:
                if self.process_event(event):
                    processed_count += 1
        return processed_count
    
    def get_events_by_supplier(self, supplier_id: str) -> List[WebhookEvent]:
        """Get all events for a specific supplier"""
        return [e for e in self.events if e.supplier_id == supplier_id]
    
    def get_events_by_type(self, event_type: WebhookEventType) -> List[WebhookEvent]:
        """Get all events of a specific type"""
        return [e for e in self.events if e.event_type == event_type]
    
    def get_unprocessed_events(self) -> List[WebhookEvent]:
        """Get all unprocessed events"""
        return [e for e in self.events if not e.processed]


# Example webhook handlers
def handle_order_update(event: WebhookEvent):
    """Example handler for order update events"""
    order_id = event.payload.get('order_id')
    status = event.payload.get('status')
    print(f"Order {order_id} updated to status: {status}")


def handle_inventory_update(event: WebhookEvent):
    """Example handler for inventory update events"""
    sku = event.payload.get('sku')
    quantity = event.payload.get('quantity')
    print(f"Inventory for {sku} updated to: {quantity}")


def handle_shipment_tracking(event: WebhookEvent):
    """Example handler for shipment tracking events"""
    tracking_number = event.payload.get('tracking_number')
    status = event.payload.get('status')
    location = event.payload.get('location')
    print(f"Shipment {tracking_number} - {status} at {location}")
