"""
Inventory Management Module for WMS
Handles inventory tracking, stock levels, and inventory operations
"""

from datetime import datetime
from typing import Dict, List, Optional


class InventoryItem:
    """Represents an inventory item in the warehouse"""
    
    def __init__(self, sku: str, name: str, quantity: int, location: str,
                 warehouse_id: str, unit_price: float = 0.0):
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.location = location
        self.warehouse_id = warehouse_id
        self.unit_price = unit_price
        self.last_updated = datetime.now()
        self.reserved_quantity = 0
        
    def available_quantity(self) -> int:
        """Returns the available quantity (not reserved)"""
        return max(0, self.quantity - self.reserved_quantity)
    
    def reserve(self, quantity: int) -> bool:
        """Reserve inventory for an order"""
        if self.available_quantity() >= quantity:
            self.reserved_quantity += quantity
            return True
        return False
    
    def release_reservation(self, quantity: int):
        """Release reserved inventory"""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            'sku': self.sku,
            'name': self.name,
            'quantity': self.quantity,
            'available_quantity': self.available_quantity(),
            'reserved_quantity': self.reserved_quantity,
            'location': self.location,
            'warehouse_id': self.warehouse_id,
            'unit_price': self.unit_price,
            'last_updated': self.last_updated.isoformat()
        }


class InventoryManager:
    """Manages warehouse inventory operations"""
    
    def __init__(self):
        self.inventory: Dict[str, InventoryItem] = {}
    
    def add_item(self, item: InventoryItem) -> bool:
        """Add or update an inventory item"""
        key = f"{item.warehouse_id}:{item.sku}"
        self.inventory[key] = item
        return True
    
    def get_item(self, warehouse_id: str, sku: str) -> Optional[InventoryItem]:
        """Get an inventory item by warehouse and SKU"""
        key = f"{warehouse_id}:{sku}"
        return self.inventory.get(key)
    
    def update_quantity(self, warehouse_id: str, sku: str, quantity: int) -> bool:
        """Update inventory quantity"""
        item = self.get_item(warehouse_id, sku)
        if item:
            item.quantity = quantity
            item.last_updated = datetime.now()
            return True
        return False
    
    def adjust_quantity(self, warehouse_id: str, sku: str, adjustment: int) -> bool:
        """Adjust inventory quantity by a delta (positive or negative)"""
        item = self.get_item(warehouse_id, sku)
        if item:
            item.quantity = max(0, item.quantity + adjustment)
            item.last_updated = datetime.now()
            return True
        return False
    
    def get_low_stock_items(self, warehouse_id: str, threshold: int = 10) -> List[InventoryItem]:
        """Get items below the stock threshold"""
        low_stock = []
        for key, item in self.inventory.items():
            if item.warehouse_id == warehouse_id and item.available_quantity() < threshold:
                low_stock.append(item)
        return low_stock
    
    def get_warehouse_inventory(self, warehouse_id: str) -> List[InventoryItem]:
        """Get all inventory items for a warehouse"""
        return [item for key, item in self.inventory.items() 
                if item.warehouse_id == warehouse_id]
    
    def transfer_inventory(self, from_warehouse: str, to_warehouse: str, 
                          sku: str, quantity: int) -> bool:
        """Transfer inventory between warehouses"""
        source_item = self.get_item(from_warehouse, sku)
        if not source_item or source_item.available_quantity() < quantity:
            return False
        
        # Reduce from source
        source_item.quantity -= quantity
        source_item.last_updated = datetime.now()
        
        # Add to destination
        dest_item = self.get_item(to_warehouse, sku)
        if dest_item:
            dest_item.quantity += quantity
            dest_item.last_updated = datetime.now()
        else:
            # Create new item at destination
            new_item = InventoryItem(
                sku=sku,
                name=source_item.name,
                quantity=quantity,
                location="",
                warehouse_id=to_warehouse,
                unit_price=source_item.unit_price
            )
            self.add_item(new_item)
        
        return True
