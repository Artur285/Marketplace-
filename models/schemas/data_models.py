"""
Data Models and Schemas for WMS/TMS System
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Product Models
class Product(BaseModel):
    """Product data model"""
    sku: str = Field(..., description="Stock Keeping Unit")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    weight: Optional[float] = Field(None, description="Weight in kg")
    length: Optional[float] = Field(None, description="Length in cm")
    width: Optional[float] = Field(None, description="Width in cm")
    height: Optional[float] = Field(None, description="Height in cm")
    unit_price: float = Field(0.0, description="Unit price")
    barcode: Optional[str] = Field(None, description="Barcode")
    active: bool = Field(True, description="Product is active")


# Inventory Models
class InventoryLocation(BaseModel):
    """Inventory location model"""
    warehouse_id: str
    zone: str
    aisle: str
    shelf: str
    bin: str
    
    def __str__(self):
        return f"{self.warehouse_id}-{self.zone}-{self.aisle}-{self.shelf}-{self.bin}"


class InventoryItem(BaseModel):
    """Inventory item model"""
    sku: str
    warehouse_id: str
    location: str
    quantity: int
    reserved_quantity: int = 0
    available_quantity: int
    last_updated: datetime
    reorder_point: int = 10
    reorder_quantity: int = 50


# Order Models
class OrderLineItem(BaseModel):
    """Order line item model"""
    line_id: str
    sku: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    picked_quantity: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "line_id": "LINE_001",
                "sku": "PROD-12345",
                "product_name": "Widget A",
                "quantity": 5,
                "unit_price": 19.99,
                "total_price": 99.95,
                "picked_quantity": 0
            }
        }


class Address(BaseModel):
    """Address model"""
    name: str
    street1: str
    street2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: Optional[str] = None
    email: Optional[str] = None


class Order(BaseModel):
    """Order model"""
    order_id: str
    warehouse_id: str
    customer_name: str
    shipping_address: Address
    billing_address: Optional[Address] = None
    lines: List[OrderLineItem]
    status: str
    total_value: float
    created_at: datetime
    updated_at: datetime
    expected_ship_date: Optional[datetime] = None
    notes: Optional[str] = None


# Shipment Models
class ShipmentTracking(BaseModel):
    """Shipment tracking model"""
    tracking_number: str
    carrier_id: str
    carrier_name: str
    status: str
    location: Optional[str] = None
    timestamp: datetime
    description: str


class Shipment(BaseModel):
    """Shipment model"""
    shipment_id: str
    order_id: str
    carrier_id: str
    tracking_number: Optional[str] = None
    origin_address: Address
    destination_address: Address
    status: str
    created_at: datetime
    updated_at: datetime
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    weight: Optional[float] = None
    cost: Optional[float] = None
    tracking_events: List[ShipmentTracking] = []


# Carrier Models
class CarrierService(BaseModel):
    """Carrier service model"""
    carrier_id: str
    carrier_name: str
    service_type: str
    base_rate: float
    per_kg_rate: float
    transit_days: int
    active: bool = True


# Supplier Models
class SupplierConfig(BaseModel):
    """Supplier configuration model"""
    supplier_id: str
    name: str
    active: bool
    api_type: str
    base_url: str
    auth_type: str
    credentials: dict
    timeout: int = 30
    capabilities: dict
    field_mappings: dict


class SupplierInventoryItem(BaseModel):
    """Supplier inventory item model"""
    supplier_id: str
    sku: str
    supplier_sku: str
    quantity: int
    price: float
    last_updated: datetime


class SupplierOrder(BaseModel):
    """Supplier order model"""
    supplier_order_id: str
    internal_order_id: str
    supplier_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderLineItem]
    total_value: float


# Webhook Models
class WebhookEvent(BaseModel):
    """Webhook event model"""
    event_id: str
    event_type: str
    supplier_id: str
    payload: dict
    signature: Optional[str] = None
    received_at: datetime
    processed: bool = False
    processed_at: Optional[datetime] = None


# API Request/Response Models
class InventoryUpdateRequest(BaseModel):
    """Inventory update request"""
    warehouse_id: str
    sku: str
    quantity: int
    location: Optional[str] = None


class OrderCreateRequest(BaseModel):
    """Order creation request"""
    warehouse_id: str
    customer_name: str
    shipping_address: Address
    lines: List[OrderLineItem]


class ShipmentCreateRequest(BaseModel):
    """Shipment creation request"""
    order_id: str
    carrier_id: str
    origin_address: Address
    destination_address: Address
    weight: Optional[float] = None


class APIResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None
    errors: Optional[List[str]] = None
