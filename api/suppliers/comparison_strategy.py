"""
Supplier Comparison and Strategy Module
Compare suppliers company-to-company for fashion categories
"""

from typing import Dict, List, Optional
from datetime import datetime
import json


class SupplierMetrics:
    """Metrics for supplier comparison"""
    
    def __init__(self, supplier_data: Dict):
        self.supplier_id = supplier_data.get('supplier_id')
        self.name = supplier_data.get('name')
        self.category = supplier_data.get('category')
        self.region = supplier_data.get('region')
        self.rating = supplier_data.get('rating', 0.0)
        self.min_order_value = supplier_data.get('min_order_value', 0)
        self.lead_time_days = supplier_data.get('lead_time_days', 0)
        self.api_quality = supplier_data.get('api_integration', {}).get('quality_score', 0)
        self.certifications_count = len(supplier_data.get('certifications', []))
        self.brands_count = len(supplier_data.get('brands', []))
        self.shipping_coverage = len(supplier_data.get('shipping_countries', []))
        
    def calculate_overall_score(self, weights: Optional[Dict] = None) -> float:
        """Calculate weighted overall score"""
        if weights is None:
            weights = {
                'rating': 0.25,
                'api_quality': 0.20,
                'lead_time': 0.20,
                'price': 0.15,
                'certifications': 0.10,
                'coverage': 0.10
            }
        
        # Normalize metrics to 0-10 scale
        rating_score = self.rating * 2  # 0-5 -> 0-10
        api_score = self.api_quality  # Already 0-10
        lead_time_score = max(0, 10 - (self.lead_time_days / 3))  # Lower is better
        price_score = max(0, 10 - (self.min_order_value / 1000))  # Lower is better
        cert_score = min(10, self.certifications_count * 2)
        coverage_score = min(10, self.shipping_coverage / 10)
        
        overall = (
            rating_score * weights['rating'] +
            api_score * weights['api_quality'] +
            lead_time_score * weights['lead_time'] +
            price_score * weights['price'] +
            cert_score * weights['certifications'] +
            coverage_score * weights['coverage']
        )
        
        return round(overall, 2)


class CompanyToCompanyComparison:
    """Compare suppliers company-to-company"""
    
    def __init__(self):
        self.suppliers_data: Dict[str, Dict] = {}
        
    def load_suppliers(self, filepath: str):
        """Load supplier data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Flatten supplier data
            for category_key in data.get('worldwide_fashion_suppliers', {}).keys():
                for supplier in data['worldwide_fashion_suppliers'][category_key]:
                    self.suppliers_data[supplier['supplier_id']] = supplier
                    
        except Exception as e:
            print(f"Error loading suppliers: {e}")
    
    def compare_by_category(self, category: str) -> List[Dict]:
        """Compare all suppliers in a category"""
        category_suppliers = [
            s for s in self.suppliers_data.values()
            if s.get('category') == category
        ]
        
        comparison_results = []
        for supplier in category_suppliers:
            metrics = SupplierMetrics(supplier)
            comparison_results.append({
                'supplier_id': supplier['supplier_id'],
                'name': supplier['name'],
                'region': supplier['region'],
                'overall_score': metrics.calculate_overall_score(),
                'metrics': {
                    'rating': metrics.rating,
                    'min_order': metrics.min_order_value,
                    'lead_time': metrics.lead_time_days,
                    'api_quality': metrics.api_quality,
                    'certifications': metrics.certifications_count,
                    'brands': metrics.brands_count
                },
                'strengths': self._identify_strengths(metrics),
                'ideal_for': self._identify_ideal_use_cases(supplier)
            })
        
        # Sort by overall score
        comparison_results.sort(key=lambda x: x['overall_score'], reverse=True)
        return comparison_results
    
    def compare_specific_suppliers(self, supplier_ids: List[str]) -> Dict:
        """Detailed comparison of specific suppliers"""
        suppliers = [
            self.suppliers_data[sid] for sid in supplier_ids 
            if sid in self.suppliers_data
        ]
        
        if not suppliers:
            return {}
        
        comparison = {
            'suppliers': [],
            'category': suppliers[0].get('category'),
            'comparison_date': datetime.now().isoformat(),
            'winner': None,
            'summary': {}
        }
        
        best_score = 0
        for supplier in suppliers:
            metrics = SupplierMetrics(supplier)
            score = metrics.calculate_overall_score()
            
            supplier_comparison = {
                'supplier_id': supplier['supplier_id'],
                'name': supplier['name'],
                'region': supplier['region'],
                'score': score,
                'details': {
                    'rating': f"{metrics.rating}/5.0",
                    'min_order_value': f"${metrics.min_order_value}",
                    'lead_time': f"{metrics.lead_time_days} days",
                    'api_quality': f"{metrics.api_quality}/10",
                    'certifications': metrics.certifications_count,
                    'brands': metrics.brands_count,
                    'shipping_coverage': f"{metrics.shipping_coverage} regions"
                },
                'advantages': self._identify_strengths(metrics),
                'best_for': self._identify_ideal_use_cases(supplier)
            }
            
            comparison['suppliers'].append(supplier_comparison)
            
            if score > best_score:
                best_score = score
                comparison['winner'] = supplier['name']
        
        # Generate summary
        comparison['summary'] = self._generate_comparison_summary(comparison['suppliers'])
        
        return comparison
    
    def get_regional_comparison(self, category: str) -> Dict:
        """Compare suppliers by region within a category"""
        regional_data = {}
        
        for supplier in self.suppliers_data.values():
            if supplier.get('category') != category:
                continue
                
            region = supplier.get('region')
            if region not in regional_data:
                regional_data[region] = []
            
            metrics = SupplierMetrics(supplier)
            regional_data[region].append({
                'name': supplier['name'],
                'score': metrics.calculate_overall_score(),
                'rating': metrics.rating,
                'lead_time': metrics.lead_time_days
            })
        
        # Calculate regional averages
        regional_summary = {}
        for region, suppliers in regional_data.items():
            if suppliers:
                regional_summary[region] = {
                    'supplier_count': len(suppliers),
                    'avg_score': round(sum(s['score'] for s in suppliers) / len(suppliers), 2),
                    'avg_rating': round(sum(s['rating'] for s in suppliers) / len(suppliers), 2),
                    'avg_lead_time': round(sum(s['lead_time'] for s in suppliers) / len(suppliers), 1),
                    'best_supplier': max(suppliers, key=lambda x: x['score'])['name']
                }
        
        return regional_summary
    
    def recommend_supplier(self, requirements: Dict) -> Optional[Dict]:
        """Recommend best supplier based on requirements"""
        category = requirements.get('category')
        max_lead_time = requirements.get('max_lead_time', 999)
        max_min_order = requirements.get('max_min_order', 999999)
        min_rating = requirements.get('min_rating', 0)
        required_region = requirements.get('region')
        required_certifications = requirements.get('certifications', [])
        
        candidates = []
        
        for supplier in self.suppliers_data.values():
            # Filter by requirements
            if supplier.get('category') != category:
                continue
            if supplier.get('lead_time_days', 999) > max_lead_time:
                continue
            if supplier.get('min_order_value', 999999) > max_min_order:
                continue
            if supplier.get('rating', 0) < min_rating:
                continue
            if required_region and supplier.get('region') != required_region:
                continue
            
            # Check certifications
            supplier_certs = supplier.get('certifications', [])
            if required_certifications:
                if not all(cert in supplier_certs for cert in required_certifications):
                    continue
            
            # Calculate custom score based on requirements
            metrics = SupplierMetrics(supplier)
            custom_weights = {
                'rating': 0.30,
                'api_quality': 0.25,
                'lead_time': 0.25,
                'price': 0.10,
                'certifications': 0.05,
                'coverage': 0.05
            }
            score = metrics.calculate_overall_score(custom_weights)
            
            candidates.append({
                'supplier': supplier,
                'score': score,
                'match_percentage': self._calculate_match_percentage(supplier, requirements)
            })
        
        if not candidates:
            return None
        
        # Return best match
        best_match = max(candidates, key=lambda x: (x['match_percentage'], x['score']))
        
        return {
            'recommended_supplier': best_match['supplier']['name'],
            'supplier_id': best_match['supplier']['supplier_id'],
            'match_percentage': best_match['match_percentage'],
            'score': best_match['score'],
            'reason': self._generate_recommendation_reason(best_match['supplier'], requirements)
        }
    
    def _identify_strengths(self, metrics: SupplierMetrics) -> List[str]:
        """Identify supplier strengths"""
        strengths = []
        
        if metrics.rating >= 4.5:
            strengths.append("Excellent customer rating")
        if metrics.api_quality >= 9.0:
            strengths.append("Premium API integration")
        if metrics.lead_time_days <= 10:
            strengths.append("Fast delivery")
        if metrics.certifications_count >= 3:
            strengths.append("Well certified")
        if metrics.brands_count >= 5:
            strengths.append("Diverse brand portfolio")
        
        return strengths
    
    def _identify_ideal_use_cases(self, supplier: Dict) -> List[str]:
        """Identify ideal use cases for supplier"""
        use_cases = []
        
        specialties = supplier.get('specialties', [])
        region = supplier.get('region')
        lead_time = supplier.get('lead_time_days', 0)
        
        if 'luxury' in ' '.join(specialties).lower():
            use_cases.append("High-end luxury market")
        if lead_time <= 10:
            use_cases.append("Quick turnaround orders")
        if region == 'europe':
            use_cases.append("European market focus")
        if supplier.get('min_order_value', 0) < 3000:
            use_cases.append("Small to medium order volumes")
        
        return use_cases
    
    def _generate_comparison_summary(self, suppliers: List[Dict]) -> Dict:
        """Generate comparison summary"""
        return {
            'total_compared': len(suppliers),
            'score_range': {
                'highest': max(s['score'] for s in suppliers),
                'lowest': min(s['score'] for s in suppliers),
                'average': round(sum(s['score'] for s in suppliers) / len(suppliers), 2)
            },
            'key_differentiators': [
                'API integration quality',
                'Lead time efficiency',
                'Order minimum requirements',
                'Certification standards'
            ]
        }
    
    def _calculate_match_percentage(self, supplier: Dict, requirements: Dict) -> float:
        """Calculate how well supplier matches requirements"""
        matches = 0
        total_criteria = 0
        
        if 'max_lead_time' in requirements:
            total_criteria += 1
            if supplier.get('lead_time_days', 999) <= requirements['max_lead_time']:
                matches += 1
        
        if 'min_rating' in requirements:
            total_criteria += 1
            if supplier.get('rating', 0) >= requirements['min_rating']:
                matches += 1
        
        if 'region' in requirements:
            total_criteria += 1
            if supplier.get('region') == requirements['region']:
                matches += 1
        
        return (matches / total_criteria * 100) if total_criteria > 0 else 100
    
    def _generate_recommendation_reason(self, supplier: Dict, requirements: Dict) -> str:
        """Generate human-readable recommendation reason"""
        reasons = []
        
        if supplier.get('rating', 0) >= 4.5:
            reasons.append("high customer satisfaction")
        
        if supplier.get('api_integration', {}).get('available'):
            reasons.append("robust API integration")
        
        if supplier.get('lead_time_days', 999) <= requirements.get('max_lead_time', 999):
            reasons.append("meets delivery timeline")
        
        return f"Recommended for {', '.join(reasons)}"
