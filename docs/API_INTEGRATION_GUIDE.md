# API Integration Guide

## Quick Start Integration

This guide explains how to integrate the WMS/TMS system with your fashion suppliers for clothing, perfume, accessories, and glasses.

## Table of Contents

1. [Setup](#setup)
2. [WMS Integration](#wms-integration)
3. [TMS Integration](#tms-integration)
4. [Supplier Integration](#supplier-integration)
5. [Comparison & Selection](#comparison--selection)
6. [API Endpoints](#api-endpoints)

## Setup

### Installation

```bash
# Install dependencies (example for Python)
pip install pydantic requests

# Configure environment
cp config/config.json config/config.local.json
# Edit config.local.json with your settings
```

### Configuration

Edit `config/config.json`:

```json
{
  "database": {
    "type": "postgresql",
    "host": "your-db-host",
    "database": "marketplace_wms_tms"
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

## WMS Integration

### 1. Inventory Management

```python
from wms.inventory.inventory_manager import InventoryManager, InventoryItem

# Initialize manager
inventory_mgr = InventoryManager()

# Add inventory item
item = InventoryItem(
    sku="SHIRT-001",
    name="Designer T-Shirt",
    quantity=100,
    location="A-01-01",
    warehouse_id="WAREHOUSE_01",
    unit_price=29.99
)
inventory_mgr.add_item(item)

# Check available quantity
available = item.available_quantity()
print(f"Available: {available}")

# Reserve inventory
success = item.reserve(5)  # Reserve 5 units
```

### 2. Order Fulfillment

```python
from wms.fulfillment.order_fulfillment import (
    OrderFulfillmentManager, FulfillmentOrder, OrderLine
)

# Initialize fulfillment manager
fulfillment_mgr = OrderFulfillmentManager(inventory_mgr)

# Create order
order = FulfillmentOrder(
    order_id="ORD-12345",
    warehouse_id="WAREHOUSE_01",
    customer_info={
        "name": "John Doe",
        "email": "john@example.com"
    }
)

# Add line items
line = OrderLine(sku="SHIRT-001", quantity=2, unit_price=29.99)
order.add_line(line)

# Create and process
fulfillment_mgr.create_order(order)
fulfillment_mgr.start_picking(order.order_id)
fulfillment_mgr.complete_picking(order.order_id)
fulfillment_mgr.ship_order(order.order_id, "TRACK123456")
```

## TMS Integration

### 1. Shipment Tracking

```python
from tms.shipment.shipment_tracker import ShipmentTracker, Shipment

# Initialize tracker
tracker = ShipmentTracker()

# Create shipment
shipment = Shipment(
    shipment_id="SHIP-001",
    order_id="ORD-12345",
    carrier_id="UPS",
    origin={"city": "New York", "country": "USA"},
    destination={"city": "Los Angeles", "country": "USA"}
)

tracker.create_shipment(shipment)
tracker.assign_tracking_number("SHIP-001", "1Z999AA10123456784")
```

### 2. Carrier Management

```python
from tms.carriers.carrier_manager import CarrierManager, Carrier

# Initialize carrier manager
carrier_mgr = CarrierManager()

# Add carrier
carrier = Carrier("UPS", "UPS Express", "express")
carrier.base_rate = 15.00
carrier.per_kg_rate = 2.50
carrier.transit_days = 2

carrier_mgr.add_carrier(carrier)

# Get rate quote
rate = carrier.calculate_rate(weight=5.0, distance=1000)
print(f"Shipping cost: ${rate}")
```

## Supplier Integration

### 1. Configure Supplier

Add to `config/suppliers/worldwide_fashion_suppliers.json`:

```json
{
  "supplier_id": "YOUR_SUPPLIER_001",
  "name": "Your Supplier Name",
  "region": "europe",
  "category": "clothing",
  "api_integration": {
    "available": true,
    "type": "rest_api",
    "base_url": "https://api.yoursupplier.com/v1"
  }
}
```

### 2. Integrate Supplier API

```python
from api.suppliers.supplier_api import RESTSupplierAdapter

# Create adapter
config = {
    'base_url': 'https://api.supplier.com/v1',
    'auth_type': 'api_key',
    'api_key': 'your-api-key-here',
    'timeout': 30
}

adapter = RESTSupplierAdapter('SUPPLIER_001', config)

# Authenticate
adapter.authenticate()

# Fetch inventory
inventory = adapter.get_inventory()

# Create order
order_data = {
    'items': [
        {'sku': 'PROD-001', 'quantity': 10}
    ],
    'shipping_address': {...}
}
result = adapter.create_order(order_data)
```

### 3. Webhook Integration

```python
from api.webhooks.webhook_handler import (
    WebhookHandler, WebhookEvent, WebhookEventType
)

# Initialize handler
webhook_handler = WebhookHandler()

# Register webhook secret
webhook_handler.register_supplier_secret('SUPPLIER_001', 'webhook_secret')

# Handle incoming webhook
event = WebhookEvent(
    event_type=WebhookEventType.INVENTORY_UPDATED,
    supplier_id='SUPPLIER_001',
    payload={'sku': 'PROD-001', 'quantity': 50},
    signature='hmac_signature_here'
)

webhook_handler.receive_event(event)
webhook_handler.process_event(event)
```

## Comparison & Selection

### 1. Compare Suppliers by Category

```python
from api.suppliers.comparison_strategy import CompanyToCompanyComparison

# Initialize comparator
comparator = CompanyToCompanyComparison()
comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')

# Compare clothing suppliers
results = comparator.compare_by_category('clothing')

for supplier in results:
    print(f"{supplier['name']}: Score {supplier['overall_score']}/10")
```

### 2. Get Recommendation

```python
# Define requirements
requirements = {
    'category': 'perfume',
    'max_lead_time': 15,
    'max_min_order': 7000,
    'min_rating': 4.5,
    'region': 'europe'
}

# Get recommendation
recommendation = comparator.recommend_supplier(requirements)

if recommendation:
    print(f"Recommended: {recommendation['recommended_supplier']}")
    print(f"Match: {recommendation['match_percentage']}%")
```

### 3. Regional Analysis

```python
# Analyze by region
regional_data = comparator.get_regional_comparison('glasses')

for region, data in regional_data.items():
    print(f"{region}: {data['supplier_count']} suppliers")
    print(f"  Best: {data['best_supplier']}")
```

## API Endpoints

### WMS Endpoints

```
POST   /api/wms/inventory          Create/update inventory
GET    /api/wms/inventory/:id      Get inventory details
GET    /api/wms/inventory/low      Get low stock items
POST   /api/wms/orders             Create order
GET    /api/wms/orders/:id         Get order status
PUT    /api/wms/orders/:id/pick    Start picking
PUT    /api/wms/orders/:id/ship    Ship order
```

### TMS Endpoints

```
POST   /api/tms/shipments          Create shipment
GET    /api/tms/shipments/:id      Get shipment details
GET    /api/tms/track/:number      Track by tracking number
POST   /api/tms/carriers           Add carrier
GET    /api/tms/carriers/:id       Get carrier info
POST   /api/tms/quotes             Get rate quotes
```

### Supplier Integration Endpoints

```
POST   /api/suppliers/sync         Sync with supplier
GET    /api/suppliers/:id/inventory Get supplier inventory
POST   /api/suppliers/:id/orders   Create supplier order
GET    /api/suppliers/:id/status   Get order status
POST   /api/webhooks/:id           Webhook receiver
GET    /api/suppliers/compare      Compare suppliers
POST   /api/suppliers/recommend    Get recommendation
```

## Request/Response Examples

### Create Inventory Item

**Request:**
```http
POST /api/wms/inventory
Content-Type: application/json

{
  "sku": "PERFUME-001",
  "name": "Luxury Fragrance",
  "warehouse_id": "WAREHOUSE_01",
  "location": "F-03-02",
  "quantity": 50,
  "unit_price": 89.99
}
```

**Response:**
```json
{
  "success": true,
  "message": "Inventory item created",
  "data": {
    "sku": "PERFUME-001",
    "available_quantity": 50
  }
}
```

### Create Shipment

**Request:**
```http
POST /api/tms/shipments
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "carrier_id": "DHL",
  "origin": {
    "city": "Paris",
    "country": "France"
  },
  "destination": {
    "city": "London",
    "country": "UK"
  },
  "weight": 2.5
}
```

**Response:**
```json
{
  "success": true,
  "message": "Shipment created",
  "data": {
    "shipment_id": "SHIP-001",
    "tracking_number": "DHL123456789",
    "estimated_delivery": "2026-01-08T12:00:00Z"
  }
}
```

### Compare Suppliers

**Request:**
```http
GET /api/suppliers/compare?category=clothing
```

**Response:**
```json
{
  "success": true,
  "data": {
    "category": "clothing",
    "suppliers": [
      {
        "supplier_id": "CLOTH_EU_001",
        "name": "European Fashion Group",
        "score": 9.2,
        "region": "europe",
        "strengths": ["Excellent rating", "Fast delivery"]
      },
      {
        "supplier_id": "CLOTH_US_001",
        "name": "American Apparel Wholesale",
        "score": 8.8,
        "region": "north_america",
        "strengths": ["Premium API", "Good coverage"]
      }
    ]
  }
}
```

## Authentication

### API Key Authentication

```http
GET /api/wms/inventory
X-API-Key: your-api-key-here
```

### OAuth 2.0 Authentication

```http
POST /api/auth/token
Content-Type: application/json

{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "grant_type": "client_credentials"
}
```

Response:
```json
{
  "access_token": "eyJhbG...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Use token:
```http
GET /api/wms/inventory
Authorization: Bearer eyJhbG...
```

## Error Handling

All API responses include error details:

```json
{
  "success": false,
  "message": "Invalid SKU",
  "errors": [
    "SKU 'INVALID-001' not found in inventory",
    "Please check SKU format"
  ]
}
```

## Rate Limiting

- Default: 60 requests per minute per API key
- Rate limit headers included in responses:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704459600
```

## Support

For integration support:
- Documentation: `/docs`
- Examples: `/docs/examples`
- Issues: GitHub repository issues

## Next Steps

1. Review [Supplier Comparison Guide](SUPPLIER_COMPARISON_GUIDE.md)
2. Run example scripts in `/docs/examples`
3. Configure your suppliers in `/config/suppliers`
4. Test API endpoints with provided examples
5. Implement webhook handlers for real-time updates
