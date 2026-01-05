"""
Order Fulfillment Module for WMS
Handles order processing, picking, packing, and shipping
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class OrderStatus(Enum):
    """Order fulfillment status"""
    PENDING = "pending"
    PICKING = "picking"
    PICKED = "picked"
    PACKING = "packing"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderLine:
    """Represents a line item in an order"""
    
    def __init__(self, sku: str, quantity: int, unit_price: float):
        self.sku = sku
        self.quantity = quantity
        self.unit_price = unit_price
        self.picked_quantity = 0
        
    def to_dict(self) -> Dict:
        return {
            'sku': self.sku,
            'quantity': self.quantity,
            'picked_quantity': self.picked_quantity,
            'unit_price': self.unit_price,
            'total_price': self.quantity * self.unit_price
        }


class FulfillmentOrder:
    """Represents a fulfillment order"""
    
    def __init__(self, order_id: str, warehouse_id: str, customer_info: Dict):
        self.order_id = order_id
        self.warehouse_id = warehouse_id
        self.customer_info = customer_info
        self.lines: List[OrderLine] = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tracking_number: Optional[str] = None
        self.notes: List[str] = []
        
    def add_line(self, line: OrderLine):
        """Add a line item to the order"""
        self.lines.append(line)
        self.updated_at = datetime.now()
        
    def get_total_value(self) -> float:
        """Calculate total order value"""
        return sum(line.quantity * line.unit_price for line in self.lines)
    
    def to_dict(self) -> Dict:
        return {
            'order_id': self.order_id,
            'warehouse_id': self.warehouse_id,
            'customer_info': self.customer_info,
            'lines': [line.to_dict() for line in self.lines],
            'status': self.status.value,
            'total_value': self.get_total_value(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tracking_number': self.tracking_number,
            'notes': self.notes
        }


class OrderFulfillmentManager:
    """Manages order fulfillment operations"""
    
    def __init__(self, inventory_manager=None):
        self.orders: Dict[str, FulfillmentOrder] = {}
        self.inventory_manager = inventory_manager
        
    def create_order(self, order: FulfillmentOrder) -> bool:
        """Create a new fulfillment order"""
        if order.order_id in self.orders:
            return False
        
        # Reserve inventory if inventory manager is available
        if self.inventory_manager:
            for line in order.lines:
                item = self.inventory_manager.get_item(order.warehouse_id, line.sku)
                if not item or not item.reserve(line.quantity):
                    # Rollback reservations
                    for prev_line in order.lines:
                        if prev_line == line:
                            break
                        prev_item = self.inventory_manager.get_item(
                            order.warehouse_id, prev_line.sku
                        )
                        if prev_item:
                            prev_item.release_reservation(prev_line.quantity)
                    return False
        
        self.orders[order.order_id] = order
        return True
    
    def get_order(self, order_id: str) -> Optional[FulfillmentOrder]:
        """Get an order by ID"""
        return self.orders.get(order_id)
    
    def update_status(self, order_id: str, status: OrderStatus) -> bool:
        """Update order status"""
        order = self.get_order(order_id)
        if order:
            order.status = status
            order.updated_at = datetime.now()
            return True
        return False
    
    def start_picking(self, order_id: str) -> bool:
        """Start picking process for an order"""
        return self.update_status(order_id, OrderStatus.PICKING)
    
    def complete_picking(self, order_id: str) -> bool:
        """Mark picking as complete"""
        order = self.get_order(order_id)
        if order and order.status == OrderStatus.PICKING:
            # Mark all lines as picked
            for line in order.lines:
                line.picked_quantity = line.quantity
            return self.update_status(order_id, OrderStatus.PICKED)
        return False
    
    def start_packing(self, order_id: str) -> bool:
        """Start packing process"""
        order = self.get_order(order_id)
        if order and order.status == OrderStatus.PICKED:
            return self.update_status(order_id, OrderStatus.PACKING)
        return False
    
    def complete_packing(self, order_id: str) -> bool:
        """Mark packing as complete"""
        return self.update_status(order_id, OrderStatus.PACKED)
    
    def ship_order(self, order_id: str, tracking_number: str) -> bool:
        """Mark order as shipped"""
        order = self.get_order(order_id)
        if order and order.status == OrderStatus.PACKED:
            order.tracking_number = tracking_number
            
            # Release reservations and reduce inventory
            if self.inventory_manager:
                for line in order.lines:
                    item = self.inventory_manager.get_item(order.warehouse_id, line.sku)
                    if item:
                        item.release_reservation(line.quantity)
            
            return self.update_status(order_id, OrderStatus.SHIPPED)
        return False
    
    def cancel_order(self, order_id: str, reason: str) -> bool:
        """Cancel an order"""
        order = self.get_order(order_id)
        if order and order.status not in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            # Release inventory reservations
            if self.inventory_manager:
                for line in order.lines:
                    item = self.inventory_manager.get_item(order.warehouse_id, line.sku)
                    if item:
                        item.release_reservation(line.quantity)
            
            order.notes.append(f"Cancelled: {reason}")
            return self.update_status(order_id, OrderStatus.CANCELLED)
        return False
