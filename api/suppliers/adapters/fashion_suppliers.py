"""
Fashion Industry Supplier Integration Strategy
Specialized adapters for clothes, perfume, accessories, and glasses suppliers
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class SupplierCategory(Enum):
    """Supplier product categories"""
    CLOTHING = "clothing"
    PERFUME = "perfume"
    ACCESSORIES = "accessories"
    GLASSES = "glasses"


class SupplierRegion(Enum):
    """Worldwide supplier regions"""
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    ASIA_PACIFIC = "asia_pacific"
    MIDDLE_EAST = "middle_east"
    LATIN_AMERICA = "latin_america"
    AFRICA = "africa"


class FashionSupplier:
    """Fashion industry supplier profile"""
    
    def __init__(self, supplier_id: str, name: str, category: SupplierCategory,
                 region: SupplierRegion):
        self.supplier_id = supplier_id
        self.name = name
        self.category = category
        self.region = region
        self.active = True
        self.rating = 0.0
        self.brands: List[str] = []
        self.min_order_value = 0.0
        self.lead_time_days = 0
        self.shipping_countries: List[str] = []
        self.certifications: List[str] = []
        self.api_integration = {
            'available': False,
            'type': None,
            'quality_score': 0.0
        }
        
    def to_dict(self) -> Dict:
        return {
            'supplier_id': self.supplier_id,
            'name': self.name,
            'category': self.category.value,
            'region': self.region.value,
            'active': self.active,
            'rating': self.rating,
            'brands': self.brands,
            'min_order_value': self.min_order_value,
            'lead_time_days': self.lead_time_days,
            'shipping_countries': self.shipping_countries,
            'certifications': self.certifications,
            'api_integration': self.api_integration
        }


class ClothingSupplierAdapter:
    """Specialized adapter for clothing suppliers"""
    
    def __init__(self, supplier: FashionSupplier):
        self.supplier = supplier
        
    def get_catalog(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get clothing catalog with fashion-specific attributes"""
        # Clothing-specific filters: size, color, gender, season, material
        catalog_filters = {
            'category': self.supplier.category.value,
            'sizes': filters.get('sizes', []) if filters else [],
            'colors': filters.get('colors', []) if filters else [],
            'gender': filters.get('gender', 'all') if filters else 'all',
            'season': filters.get('season', 'all') if filters else 'all',
            'material': filters.get('material', []) if filters else []
        }
        
        # Template for clothing product
        return [{
            'sku': 'CLOTHING_001',
            'name': 'Designer T-Shirt',
            'brand': 'Example Brand',
            'category': 'tops',
            'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
            'colors': ['black', 'white', 'navy', 'red'],
            'gender': 'unisex',
            'season': 'all-season',
            'material': '100% cotton',
            'price': 29.99,
            'stock': 500,
            'images': []
        }]
    
    def sync_inventory(self) -> Dict:
        """Sync clothing inventory with size/color variants"""
        return {
            'supplier_id': self.supplier.supplier_id,
            'category': 'clothing',
            'sync_time': datetime.now().isoformat(),
            'items_synced': 0,
            'variants_tracked': True
        }


class PerfumeSupplierAdapter:
    """Specialized adapter for perfume suppliers"""
    
    def __init__(self, supplier: FashionSupplier):
        self.supplier = supplier
        
    def get_catalog(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get perfume catalog with fragrance-specific attributes"""
        catalog_filters = {
            'category': self.supplier.category.value,
            'fragrance_family': filters.get('fragrance_family', []) if filters else [],
            'gender': filters.get('gender', 'all') if filters else 'all',
            'size_ml': filters.get('size_ml', []) if filters else [],
            'concentration': filters.get('concentration', []) if filters else []
        }
        
        # Template for perfume product
        return [{
            'sku': 'PERFUME_001',
            'name': 'Luxury Fragrance',
            'brand': 'Example Brand',
            'category': 'perfume',
            'fragrance_family': 'oriental',
            'gender': 'women',
            'size_ml': [30, 50, 100],
            'concentration': 'eau_de_parfum',
            'notes': {
                'top': ['bergamot', 'rose'],
                'middle': ['jasmine', 'ylang-ylang'],
                'base': ['musk', 'vanilla']
            },
            'price': 89.99,
            'stock': 200,
            'batch_certified': True
        }]
    
    def verify_authenticity(self, sku: str, batch_number: str) -> bool:
        """Verify perfume authenticity"""
        # Integration with brand authentication systems
        return True


class AccessoriesSupplierAdapter:
    """Specialized adapter for accessories suppliers"""
    
    def __init__(self, supplier: FashionSupplier):
        self.supplier = supplier
        
    def get_catalog(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get accessories catalog"""
        catalog_filters = {
            'category': self.supplier.category.value,
            'accessory_type': filters.get('accessory_type', []) if filters else [],
            'material': filters.get('material', []) if filters else [],
            'gender': filters.get('gender', 'all') if filters else 'all',
            'color': filters.get('color', []) if filters else []
        }
        
        # Template for accessory product
        return [{
            'sku': 'ACCESSORY_001',
            'name': 'Leather Handbag',
            'brand': 'Example Brand',
            'category': 'bags',
            'accessory_type': 'handbag',
            'material': 'genuine_leather',
            'gender': 'women',
            'colors': ['black', 'brown', 'tan'],
            'dimensions': {'length': 30, 'width': 15, 'height': 25},
            'price': 199.99,
            'stock': 75
        }]


class GlassesSupplierAdapter:
    """Specialized adapter for eyewear suppliers"""
    
    def __init__(self, supplier: FashionSupplier):
        self.supplier = supplier
        
    def get_catalog(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get eyewear catalog with optical specifications"""
        catalog_filters = {
            'category': self.supplier.category.value,
            'type': filters.get('type', 'all') if filters else 'all',  # sunglasses, prescription
            'frame_material': filters.get('frame_material', []) if filters else [],
            'lens_type': filters.get('lens_type', []) if filters else [],
            'gender': filters.get('gender', 'all') if filters else 'all'
        }
        
        # Template for eyewear product
        return [{
            'sku': 'GLASSES_001',
            'name': 'Classic Aviator Sunglasses',
            'brand': 'Example Brand',
            'category': 'sunglasses',
            'type': 'sunglasses',
            'frame_material': 'metal',
            'frame_color': 'gold',
            'lens_type': 'polarized',
            'lens_color': 'gray',
            'uv_protection': 'UV400',
            'prescription_available': True,
            'gender': 'unisex',
            'dimensions': {
                'lens_width': 58,
                'bridge': 14,
                'temple_length': 135
            },
            'price': 149.99,
            'stock': 150,
            'certifications': ['CE', 'UV400']
        }]
    
    def check_prescription_compatibility(self, sku: str) -> Dict:
        """Check if frames are compatible with prescription lenses"""
        return {
            'compatible': True,
            'max_prescription': {'sphere': 8.0, 'cylinder': 4.0},
            'lens_options': ['single_vision', 'progressive', 'bifocal']
        }


class SupplierComparisonEngine:
    """Engine to compare suppliers across categories"""
    
    def __init__(self):
        self.suppliers: Dict[str, FashionSupplier] = {}
        
    def add_supplier(self, supplier: FashionSupplier):
        """Add a supplier to comparison database"""
        self.suppliers[supplier.supplier_id] = supplier
        
    def compare_suppliers(self, category: SupplierCategory, 
                         criteria: Optional[Dict] = None) -> List[Dict]:
        """Compare suppliers by category and criteria"""
        category_suppliers = [
            s for s in self.suppliers.values() 
            if s.category == category and s.active
        ]
        
        if not category_suppliers:
            return []
        
        comparison_results = []
        for supplier in category_suppliers:
            score = self._calculate_supplier_score(supplier, criteria)
            comparison_results.append({
                'supplier': supplier.to_dict(),
                'comparison_score': score,
                'strengths': self._identify_strengths(supplier),
                'weaknesses': self._identify_weaknesses(supplier)
            })
        
        # Sort by comparison score
        comparison_results.sort(key=lambda x: x['comparison_score'], reverse=True)
        return comparison_results
    
    def compare_by_region(self, category: SupplierCategory,
                         region: SupplierRegion) -> List[Dict]:
        """Compare suppliers by category and region"""
        regional_suppliers = [
            s for s in self.suppliers.values()
            if s.category == category and s.region == region and s.active
        ]
        
        return [s.to_dict() for s in regional_suppliers]
    
    def get_best_supplier(self, category: SupplierCategory,
                         requirements: Dict) -> Optional[FashionSupplier]:
        """Get the best supplier based on specific requirements"""
        candidates = self.compare_suppliers(category, requirements)
        return self.suppliers.get(candidates[0]['supplier']['supplier_id']) if candidates else None
    
    def compare_pricing(self, category: SupplierCategory,
                       sku_pattern: Optional[str] = None) -> List[Dict]:
        """Compare pricing across suppliers for similar products"""
        pricing_comparison = []
        
        for supplier in self.suppliers.values():
            if supplier.category == category and supplier.active:
                pricing_comparison.append({
                    'supplier_id': supplier.supplier_id,
                    'supplier_name': supplier.name,
                    'region': supplier.region.value,
                    'min_order_value': supplier.min_order_value,
                    'lead_time_days': supplier.lead_time_days,
                    'rating': supplier.rating
                })
        
        return sorted(pricing_comparison, key=lambda x: x['min_order_value'])
    
    def get_worldwide_coverage(self, category: SupplierCategory) -> Dict:
        """Analyze worldwide supplier coverage for a category"""
        coverage = {}
        
        for region in SupplierRegion:
            regional_suppliers = [
                s for s in self.suppliers.values()
                if s.category == category and s.region == region and s.active
            ]
            coverage[region.value] = {
                'supplier_count': len(regional_suppliers),
                'suppliers': [s.name for s in regional_suppliers],
                'avg_lead_time': sum(s.lead_time_days for s in regional_suppliers) / len(regional_suppliers) if regional_suppliers else 0,
                'avg_rating': sum(s.rating for s in regional_suppliers) / len(regional_suppliers) if regional_suppliers else 0
            }
        
        return coverage
    
    def _calculate_supplier_score(self, supplier: FashionSupplier,
                                  criteria: Optional[Dict]) -> float:
        """Calculate overall supplier score"""
        score = 0.0
        
        # Base score from rating
        score += supplier.rating * 20
        
        # API integration bonus
        if supplier.api_integration['available']:
            score += supplier.api_integration['quality_score'] * 10
        
        # Lead time score (inverse - lower is better)
        if supplier.lead_time_days > 0:
            score += max(0, (30 - supplier.lead_time_days)) / 30 * 20
        
        # Certification bonus
        score += len(supplier.certifications) * 5
        
        # Brand portfolio bonus
        score += min(len(supplier.brands) * 2, 20)
        
        # Custom criteria
        if criteria:
            if 'required_certifications' in criteria:
                has_all = all(cert in supplier.certifications 
                            for cert in criteria['required_certifications'])
                score += 10 if has_all else -10
            
            if 'max_lead_time' in criteria:
                if supplier.lead_time_days <= criteria['max_lead_time']:
                    score += 15
        
        return min(score, 100)
    
    def _identify_strengths(self, supplier: FashionSupplier) -> List[str]:
        """Identify supplier strengths"""
        strengths = []
        
        if supplier.rating >= 4.5:
            strengths.append("Excellent supplier rating")
        
        if supplier.api_integration['available'] and supplier.api_integration['quality_score'] >= 8:
            strengths.append("High-quality API integration")
        
        if supplier.lead_time_days <= 7:
            strengths.append("Fast delivery times")
        
        if len(supplier.brands) >= 10:
            strengths.append("Extensive brand portfolio")
        
        if len(supplier.certifications) >= 3:
            strengths.append("Well-certified supplier")
        
        if len(supplier.shipping_countries) >= 50:
            strengths.append("Worldwide shipping coverage")
        
        return strengths
    
    def _identify_weaknesses(self, supplier: FashionSupplier) -> List[str]:
        """Identify supplier weaknesses"""
        weaknesses = []
        
        if supplier.rating < 3.5:
            weaknesses.append("Below average rating")
        
        if not supplier.api_integration['available']:
            weaknesses.append("No API integration available")
        
        if supplier.lead_time_days > 21:
            weaknesses.append("Long lead times")
        
        if supplier.min_order_value > 10000:
            weaknesses.append("High minimum order value")
        
        if len(supplier.certifications) == 0:
            weaknesses.append("No certifications")
        
        return weaknesses
