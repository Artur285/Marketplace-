"""
Supplier API Integration Interface
Defines the base interface for supplier integrations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime


class SupplierAPIInterface(ABC):
    """Base interface for supplier API integrations"""
    
    def __init__(self, supplier_id: str, config: Dict):
        self.supplier_id = supplier_id
        self.config = config
        self.base_url = config.get('base_url', '')
        self.timeout = config.get('timeout', 30)
        
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the supplier API"""
        pass
    
    @abstractmethod
    def get_inventory(self) -> List[Dict]:
        """Fetch inventory from supplier"""
        pass
    
    @abstractmethod
    def create_order(self, order_data: Dict) -> Dict:
        """Create an order with the supplier"""
        pass
    
    @abstractmethod
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status from supplier"""
        pass
    
    @abstractmethod
    def get_tracking_info(self, tracking_number: str) -> Dict:
        """Get tracking information from supplier"""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order with supplier"""
        pass
    
    def test_connection(self) -> bool:
        """Test connection to supplier API"""
        try:
            return self.authenticate()
        except Exception:
            return False


class RESTSupplierAdapter(SupplierAPIInterface):
    """REST API adapter for supplier integrations"""
    
    def __init__(self, supplier_id: str, config: Dict):
        super().__init__(supplier_id, config)
        self.auth_token: Optional[str] = None
        self.auth_expires: Optional[datetime] = None
        
    def authenticate(self) -> bool:
        """Authenticate using API key or OAuth"""
        auth_type = self.config.get('auth_type', 'api_key')
        
        if auth_type == 'api_key':
            # API key authentication
            self.auth_token = self.config.get('api_key')
            return self.auth_token is not None
        
        elif auth_type == 'oauth2':
            # OAuth 2.0 authentication (simplified)
            # In production, implement full OAuth flow
            return False
        
        return False
    
    def _get_headers(self) -> Dict:
        """Get HTTP headers with authentication"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Marketplace-WMS-TMS/1.0'
        }
        
        if self.auth_token:
            auth_type = self.config.get('auth_type', 'api_key')
            if auth_type == 'api_key':
                headers['X-API-Key'] = self.auth_token
            elif auth_type == 'oauth2':
                headers['Authorization'] = f'Bearer {self.auth_token}'
        
        return headers
    
    def get_inventory(self) -> List[Dict]:
        """Fetch inventory from supplier via REST API"""
        # This is a template - actual implementation depends on supplier API
        endpoint = f"{self.base_url}/inventory"
        
        # In production, use requests library to make HTTP call
        # response = requests.get(endpoint, headers=self._get_headers(), timeout=self.timeout)
        # return response.json()
        
        return []
    
    def create_order(self, order_data: Dict) -> Dict:
        """Create an order with the supplier via REST API"""
        endpoint = f"{self.base_url}/orders"
        
        # Transform order data to supplier format
        transformed_data = self._transform_order_data(order_data)
        
        # In production, use requests library
        # response = requests.post(endpoint, json=transformed_data, 
        #                         headers=self._get_headers(), timeout=self.timeout)
        # return response.json()
        
        return {'order_id': 'SAMPLE_ORDER_ID', 'status': 'created'}
    
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status from supplier"""
        endpoint = f"{self.base_url}/orders/{order_id}"
        
        # In production, use requests library
        # response = requests.get(endpoint, headers=self._get_headers(), timeout=self.timeout)
        # return response.json()
        
        return {'order_id': order_id, 'status': 'processing'}
    
    def get_tracking_info(self, tracking_number: str) -> Dict:
        """Get tracking information from supplier"""
        endpoint = f"{self.base_url}/tracking/{tracking_number}"
        
        # In production, use requests library
        # response = requests.get(endpoint, headers=self._get_headers(), timeout=self.timeout)
        # return response.json()
        
        return {'tracking_number': tracking_number, 'status': 'in_transit'}
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order with supplier"""
        endpoint = f"{self.base_url}/orders/{order_id}/cancel"
        
        # In production, use requests library
        # response = requests.post(endpoint, headers=self._get_headers(), timeout=self.timeout)
        # return response.status_code == 200
        
        return True
    
    def _transform_order_data(self, order_data: Dict) -> Dict:
        """Transform internal order format to supplier format"""
        # This should be customized per supplier
        return order_data


class SupplierIntegrationManager:
    """Manages multiple supplier integrations"""
    
    def __init__(self):
        self.suppliers: Dict[str, SupplierAPIInterface] = {}
        
    def register_supplier(self, supplier: SupplierAPIInterface):
        """Register a supplier integration"""
        self.suppliers[supplier.supplier_id] = supplier
        
    def get_supplier(self, supplier_id: str) -> Optional[SupplierAPIInterface]:
        """Get a supplier integration"""
        return self.suppliers.get(supplier_id)
    
    def sync_inventory(self, supplier_id: str) -> List[Dict]:
        """Sync inventory from a supplier"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            return supplier.get_inventory()
        return []
    
    def sync_all_inventory(self) -> Dict[str, List[Dict]]:
        """Sync inventory from all suppliers"""
        results = {}
        for supplier_id, supplier in self.suppliers.items():
            try:
                results[supplier_id] = supplier.get_inventory()
            except Exception as e:
                results[supplier_id] = {'error': str(e)}
        return results
    
    def create_order_with_supplier(self, supplier_id: str, order_data: Dict) -> Dict:
        """Create an order with a specific supplier"""
        supplier = self.get_supplier(supplier_id)
        if supplier:
            return supplier.create_order(order_data)
        return {'error': 'Supplier not found'}
    
    def test_all_connections(self) -> Dict[str, bool]:
        """Test connections to all suppliers"""
        results = {}
        for supplier_id, supplier in self.suppliers.items():
            results[supplier_id] = supplier.test_connection()
        return results
