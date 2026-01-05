"""
Example Usage: Supplier Comparison and Integration
Demonstrates how to use the WMS/TMS system with fashion supplier comparisons
"""

from api.suppliers.comparison_strategy import CompanyToCompanyComparison
from api.suppliers.adapters.fashion_suppliers import (
    FashionSupplier, SupplierCategory, SupplierRegion,
    ClothingSupplierAdapter, PerfumeSupplierAdapter,
    AccessoriesSupplierAdapter, GlassesSupplierAdapter,
    SupplierComparisonEngine
)


def example_1_compare_all_clothing_suppliers():
    """Example 1: Compare all clothing suppliers"""
    print("=" * 80)
    print("EXAMPLE 1: Compare All Clothing Suppliers")
    print("=" * 80)
    
    comparator = CompanyToCompanyComparison()
    comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')
    
    results = comparator.compare_by_category('clothing')
    
    print(f"\nFound {len(results)} clothing suppliers\n")
    
    for i, supplier in enumerate(results, 1):
        print(f"{i}. {supplier['name']} ({supplier['region']})")
        print(f"   Overall Score: {supplier['overall_score']}/10")
        print(f"   Rating: {supplier['metrics']['rating']}/5")
        print(f"   Min Order: ${supplier['metrics']['min_order']}")
        print(f"   Lead Time: {supplier['metrics']['lead_time']} days")
        print(f"   API Quality: {supplier['metrics']['api_quality']}/10")
        print(f"   Strengths: {', '.join(supplier['strengths'])}")
        print(f"   Best For: {', '.join(supplier['ideal_for'])}")
        print()


def example_2_direct_supplier_comparison():
    """Example 2: Compare specific suppliers head-to-head"""
    print("=" * 80)
    print("EXAMPLE 2: Direct Supplier Comparison - Top 3 Clothing Suppliers")
    print("=" * 80)
    
    comparator = CompanyToCompanyComparison()
    comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')
    
    comparison = comparator.compare_specific_suppliers([
        'CLOTH_EU_001',   # European Fashion Group
        'CLOTH_ASIA_001', # Asia Pacific Textiles
        'CLOTH_US_001'    # American Apparel Wholesale
    ])
    
    print(f"\nCategory: {comparison['category'].upper()}")
    print(f"Winner: {comparison['winner']}\n")
    
    print("Detailed Comparison:")
    print("-" * 80)
    
    for supplier in comparison['suppliers']:
        print(f"\n{supplier['name']} (Score: {supplier['score']}/10)")
        print(f"Region: {supplier['region']}")
        print("\nMetrics:")
        for key, value in supplier['details'].items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        print(f"\nAdvantages:")
        for adv in supplier['advantages']:
            print(f"  ✓ {adv}")
        print(f"\nBest For:")
        for use in supplier['best_for']:
            print(f"  → {use}")
    
    print("\n" + "=" * 80)
    print("Summary:")
    summary = comparison['summary']
    print(f"Total Suppliers Compared: {summary['total_compared']}")
    print(f"Score Range: {summary['score_range']['lowest']:.1f} - {summary['score_range']['highest']:.1f}")
    print(f"Average Score: {summary['score_range']['average']:.1f}")


def example_3_regional_analysis():
    """Example 3: Regional supplier analysis"""
    print("=" * 80)
    print("EXAMPLE 3: Regional Analysis - Perfume Suppliers")
    print("=" * 80)
    
    comparator = CompanyToCompanyComparison()
    comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')
    
    regional_data = comparator.get_regional_comparison('perfume')
    
    print("\nPerfume Suppliers by Region:\n")
    
    for region, data in regional_data.items():
        print(f"{region.replace('_', ' ').upper()}:")
        print(f"  Suppliers Available: {data['supplier_count']}")
        print(f"  Average Score: {data['avg_score']}/10")
        print(f"  Average Rating: {data['avg_rating']}/5")
        print(f"  Average Lead Time: {data['avg_lead_time']} days")
        print(f"  Best Supplier: {data['best_supplier']}")
        print()


def example_4_smart_recommendation():
    """Example 4: Get AI-powered supplier recommendation"""
    print("=" * 80)
    print("EXAMPLE 4: Smart Supplier Recommendation")
    print("=" * 80)
    
    comparator = CompanyToCompanyComparison()
    comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')
    
    # Scenario 1: Fast turnaround eyewear needed
    print("\nScenario 1: Fast Turnaround Eyewear Supplier")
    print("-" * 80)
    
    requirements_1 = {
        'category': 'glasses',
        'max_lead_time': 12,
        'max_min_order': 5000,
        'min_rating': 4.5,
        'certifications': ['UV400']
    }
    
    print("Requirements:")
    print(f"  - Category: Glasses")
    print(f"  - Max Lead Time: 12 days")
    print(f"  - Max Minimum Order: $5,000")
    print(f"  - Min Rating: 4.5/5")
    print(f"  - Required Certifications: UV400")
    
    rec = comparator.recommend_supplier(requirements_1)
    
    if rec:
        print(f"\nRecommendation:")
        print(f"  ✓ Supplier: {rec['recommended_supplier']}")
        print(f"  ✓ Supplier ID: {rec['supplier_id']}")
        print(f"  ✓ Match: {rec['match_percentage']:.0f}%")
        print(f"  ✓ Score: {rec['score']}/10")
        print(f"  ✓ Reason: {rec['reason']}")
    else:
        print("\n✗ No suppliers match these requirements")
    
    # Scenario 2: Luxury perfume supplier
    print("\n\nScenario 2: Luxury Perfume Supplier")
    print("-" * 80)
    
    requirements_2 = {
        'category': 'perfume',
        'max_lead_time': 10,
        'min_rating': 4.8,
        'region': 'europe',
        'certifications': ['IFRA']
    }
    
    print("Requirements:")
    print(f"  - Category: Perfume")
    print(f"  - Max Lead Time: 10 days")
    print(f"  - Min Rating: 4.8/5")
    print(f"  - Region: Europe")
    print(f"  - Required Certifications: IFRA")
    
    rec = comparator.recommend_supplier(requirements_2)
    
    if rec:
        print(f"\nRecommendation:")
        print(f"  ✓ Supplier: {rec['recommended_supplier']}")
        print(f"  ✓ Supplier ID: {rec['supplier_id']}")
        print(f"  ✓ Match: {rec['match_percentage']:.0f}%")
        print(f"  ✓ Score: {rec['score']}/10")
        print(f"  ✓ Reason: {rec['reason']}")
    else:
        print("\n✗ No suppliers match these requirements")


def example_5_category_by_category_analysis():
    """Example 5: Analyze all categories"""
    print("=" * 80)
    print("EXAMPLE 5: Complete Category Analysis")
    print("=" * 80)
    
    comparator = CompanyToCompanyComparison()
    comparator.load_suppliers('config/suppliers/worldwide_fashion_suppliers.json')
    
    categories = ['clothing', 'perfume', 'accessories', 'glasses']
    
    for category in categories:
        print(f"\n{category.upper()} SUPPLIERS")
        print("-" * 80)
        
        results = comparator.compare_by_category(category)
        
        if results:
            best = results[0]
            print(f"Total Suppliers: {len(results)}")
            print(f"\nTop Supplier: {best['name']}")
            print(f"  Score: {best['overall_score']}/10")
            print(f"  Region: {best['region']}")
            print(f"  Rating: {best['metrics']['rating']}/5")
            print(f"  Lead Time: {best['metrics']['lead_time']} days")
            print(f"  Min Order: ${best['metrics']['min_order']}")
            
            if len(results) > 1:
                print(f"\nOther Options:")
                for supplier in results[1:]:
                    print(f"  - {supplier['name']} ({supplier['region']}) - Score: {supplier['overall_score']}/10")
        else:
            print(f"No suppliers found for {category}")


def example_6_fashion_supplier_engine():
    """Example 6: Using the Fashion Supplier Engine"""
    print("=" * 80)
    print("EXAMPLE 6: Fashion Supplier Comparison Engine")
    print("=" * 80)
    
    engine = SupplierComparisonEngine()
    
    # Add sample suppliers
    supplier1 = FashionSupplier(
        'TEST_EU_001',
        'Premium European Fashion',
        SupplierCategory.CLOTHING,
        SupplierRegion.EUROPE
    )
    supplier1.rating = 4.8
    supplier1.lead_time_days = 12
    supplier1.min_order_value = 5000
    supplier1.brands = ['Brand A', 'Brand B', 'Brand C']
    supplier1.certifications = ['OEKO-TEX', 'GOTS', 'Fair Trade']
    supplier1.api_integration = {'available': True, 'quality_score': 9.2}
    
    supplier2 = FashionSupplier(
        'TEST_ASIA_001',
        'Asia Manufacturing Hub',
        SupplierCategory.CLOTHING,
        SupplierRegion.ASIA_PACIFIC
    )
    supplier2.rating = 4.2
    supplier2.lead_time_days = 25
    supplier2.min_order_value = 2000
    supplier2.brands = ['Brand X', 'Brand Y']
    supplier2.certifications = ['ISO 9001']
    supplier2.api_integration = {'available': True, 'quality_score': 7.5}
    
    engine.add_supplier(supplier1)
    engine.add_supplier(supplier2)
    
    # Compare suppliers
    print("\nComparing Clothing Suppliers:")
    comparison = engine.compare_suppliers(SupplierCategory.CLOTHING)
    
    for result in comparison:
        supplier_data = result['supplier']
        print(f"\n{supplier_data['name']}:")
        print(f"  Score: {result['comparison_score']:.1f}/100")
        print(f"  Region: {supplier_data['region']}")
        print(f"  Rating: {supplier_data['rating']}/5")
        print(f"  Lead Time: {supplier_data['lead_time_days']} days")
        print(f"  Strengths: {', '.join(result['strengths'])}")
        if result['weaknesses']:
            print(f"  Weaknesses: {', '.join(result['weaknesses'])}")
    
    # Get best supplier
    print("\n" + "-" * 80)
    best = engine.get_best_supplier(SupplierCategory.CLOTHING, {})
    if best:
        print(f"\nBest Overall: {best.name}")
        print(f"  Supplier ID: {best.supplier_id}")
        print(f"  Region: {best.region.value}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "WMS/TMS SUPPLIER COMPARISON EXAMPLES" + " " * 26 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    examples = [
        ("Compare All Clothing Suppliers", example_1_compare_all_clothing_suppliers),
        ("Direct Supplier Comparison", example_2_direct_supplier_comparison),
        ("Regional Analysis", example_3_regional_analysis),
        ("Smart Recommendation", example_4_smart_recommendation),
        ("Category-by-Category Analysis", example_5_category_by_category_analysis),
        ("Fashion Supplier Engine", example_6_fashion_supplier_engine),
    ]
    
    for i, (title, func) in enumerate(examples, 1):
        print(f"\nRunning Example {i}: {title}")
        input("Press Enter to continue...")
        func()
        print("\n" + "=" * 80 + "\n")
    
    print("\n✓ All examples completed successfully!")
    print("\nFor more information, see docs/SUPPLIER_COMPARISON_GUIDE.md")


if __name__ == "__main__":
    main()
