#!/usr/bin/env python3
"""
E-Commerce Data Query Processor and Explorer
============================================

A comprehensive tool for loading, exploring, and querying e-commerce product data.
This mini-parser provides various operations to analyze product information and
can serve as a foundation for a larger e-commerce search system.

Author: Your Name
Date: 2025
Project: E-Commerce Query Processor
"""

import json
import re
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from collections import defaultdict, Counter
import statistics
from datetime import datetime
import operator


class ECommerceQueryProcessor:
    """
    A comprehensive e-commerce data processor that provides various operations
    for loading, exploring, and querying product data.
    """
    
    def __init__(self, data_file: str = None):
        """Initialize the processor with optional data file."""
        self.data = []
        self.df = None
        self.product_stats = {}
        self.search_index = defaultdict(set)
        
        if data_file:
            self.load_data(data_file)
    
    def load_data(self, file_path: str) -> bool:
        """
        Load product data from JSON file.
        
        Args:
            file_path (str): Path to the JSON data file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Loading data from {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            
            # Convert to pandas DataFrame for easier manipulation
            self.df = pd.DataFrame(self.data)
            
            # Build search index
            self._build_search_index()
            
            print(f"✅ Successfully loaded {len(self.data)} products")
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: File {file_path} not found")
            return False
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON format in {file_path}")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False
    
    def _build_search_index(self):
        """Build an inverted index for fast text searching."""
        print("Building search index...")
        for idx, product in enumerate(self.data):
            for key, value in product.items():
                if isinstance(value, str):
                    # Tokenize and index words
                    words = re.findall(r'\b\w+\b', value.lower())
                    for word in words:
                        self.search_index[word].add(idx)
        print(f"✅ Search index built with {len(self.search_index)} terms")
    
    def explore_data_structure(self):
        """Explore and analyze the structure of the dataset."""
        print("\n" + "="*60)
        print("📊 DATA STRUCTURE EXPLORATION")
        print("="*60)
        
        if not self.data:
            print("❌ No data loaded")
            return
        
        # Basic statistics
        print(f"📈 Total Products: {len(self.data)}")
        print(f"📈 Total Columns/Attributes: {len(self.df.columns)}")
        
        # Analyze attributes
        all_keys = set()
        key_frequency = Counter()
        
        for product in self.data:
            product_keys = set(product.keys())
            all_keys.update(product_keys)
            key_frequency.update(product_keys)
        
        print(f"📈 Unique Attributes Found: {len(all_keys)}")
        
        # Most common attributes
        print("\n🔝 Most Common Attributes:")
        for key, count in key_frequency.most_common(15):
            percentage = (count / len(self.data)) * 100
            print(f"   • {key}: {count} products ({percentage:.1f}%)")
        
        # Least common attributes
        print("\n🔻 Least Common Attributes:")
        for key, count in key_frequency.most_common()[-10:]:
            percentage = (count / len(self.data)) * 100
            print(f"   • {key}: {count} products ({percentage:.1f}%)")
        
        # Sample products with most attributes
        max_attrs = max(len(product.keys()) for product in self.data)
        min_attrs = min(len(product.keys()) for product in self.data)
        
        print(f"\n📏 Attribute Range:")
        print(f"   • Maximum attributes in single product: {max_attrs}")
        print(f"   • Minimum attributes in single product: {min_attrs}")
        
        return {
            'total_products': len(self.data),
            'unique_attributes': len(all_keys),
            'attribute_frequency': dict(key_frequency),
            'max_attributes': max_attrs,
            'min_attributes': min_attrs
        }
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for products using text query.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results
            
        Returns:
            List[Dict]: Matching products
        """
        print(f"\n🔍 Searching for: '{query}'")
        
        query_words = re.findall(r'\b\w+\b', query.lower())
        if not query_words:
            return []
        
        # Find products that contain any of the query words
        matching_indices = set()
        for word in query_words:
            if word in self.search_index:
                matching_indices.update(self.search_index[word])
        
        # Score products based on word matches
        scored_products = []
        for idx in matching_indices:
            product = self.data[idx]
            score = 0
            
            for key, value in product.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for word in query_words:
                        score += value_lower.count(word)
            
            scored_products.append((score, product))
        
        # Sort by score and return top results
        scored_products.sort(reverse=True, key=lambda x: x[0])
        results = [product for score, product in scored_products[:limit]]
        
        print(f"✅ Found {len(results)} matching products")
        return results
    
    def filter_products(self, filters: Dict[str, Any]) -> List[Dict]:
        """
        Filter products based on attribute criteria.
        
        Args:
            filters (Dict): Filter criteria {attribute: value/condition}
            
        Returns:
            List[Dict]: Filtered products
        """
        print(f"\n🎯 Filtering products with criteria: {filters}")
        
        filtered_products = []
        
        for product in self.data:
            match = True
            
            for attr, condition in filters.items():
                if attr not in product:
                    match = False
                    break
                
                product_value = product[attr]
                
                # Handle different condition types
                if isinstance(condition, str):
                    if condition.lower() not in product_value.lower():
                        match = False
                        break
                elif isinstance(condition, dict):
                    # Handle range conditions like {'min': 10, 'max': 100}
                    if 'min' in condition or 'max' in condition:
                        try:
                            numeric_value = self._extract_numeric_value(product_value)
                            if numeric_value is not None:
                                if 'min' in condition and numeric_value < condition['min']:
                                    match = False
                                    break
                                if 'max' in condition and numeric_value > condition['max']:
                                    match = False
                                    break
                        except:
                            match = False
                            break
                elif product_value != condition:
                    match = False
                    break
            
            if match:
                filtered_products.append(product)
        
        print(f"✅ Found {len(filtered_products)} products matching filters")
        return filtered_products
    
    def _extract_numeric_value(self, text: str) -> Optional[float]:
        """Extract numeric value from text."""
        if isinstance(text, (int, float)):
            return float(text)
        
        if isinstance(text, str):
            # Look for numbers in the text
            numbers = re.findall(r'\d+\.?\d*', text)
            if numbers:
                return float(numbers[0])
        
        return None
    
    def analyze_categories(self):
        """Analyze product categories and types."""
        print("\n" + "="*60)
        print("📂 CATEGORY ANALYSIS")
        print("="*60)
        
        # Analyze 'Type' field
        if 'Type' in self.df.columns:
            type_counts = self.df['Type'].value_counts()
            print("🏷️  Product Types:")
            for product_type, count in type_counts.head(15).items():
                if pd.notna(product_type):
                    print(f"   • {product_type}: {count} products")
        
        # Analyze 'Brand' field
        if 'Brand' in self.df.columns:
            brand_counts = self.df['Brand'].value_counts()
            print(f"\n🏢 Top Brands:")
            for brand, count in brand_counts.head(10).items():
                if pd.notna(brand):
                    print(f"   • {brand}: {count} products")
        
        # Analyze common features
        feature_keywords = ['bluetooth', 'wireless', 'portable', 'waterproof', 'led']
        print(f"\n🎯 Feature Analysis:")
        
        for keyword in feature_keywords:
            count = 0
            for product in self.data:
                for key, value in product.items():
                    if isinstance(value, str) and keyword.lower() in value.lower():
                        count += 1
                        break
            print(f"   • {keyword.title()}: {count} products")
    
    def analyze_pricing_and_weights(self):
        """Analyze pricing, weights, and numeric attributes."""
        print("\n" + "="*60)
        print("💰 PRICING & WEIGHT ANALYSIS")
        print("="*60)
        
        # Extract weight information
        weights = []
        for product in self.data:
            for key in ['Weight', 'Net Weight']:
                if key in product:
                    weight_value = self._extract_numeric_value(product[key])
                    if weight_value:
                        weights.append(weight_value)
                        break
        
        if weights:
            print(f"⚖️  Weight Statistics ({len(weights)} products):")
            print(f"   • Average: {statistics.mean(weights):.2f}")
            print(f"   • Median: {statistics.median(weights):.2f}")
            print(f"   • Min: {min(weights):.2f}")
            print(f"   • Max: {max(weights):.2f}")
        
        # Analyze warranty information
        warranty_counts = {}
        for product in self.data:
            for key in ['Domestic Warranty', 'Warranty']:
                if key in product:
                    warranty = product[key]
                    warranty_counts[warranty] = warranty_counts.get(warranty, 0) + 1
                    break
        
        if warranty_counts:
            print(f"\n🛡️  Warranty Information:")
            for warranty, count in sorted(warranty_counts.items(), 
                                        key=lambda x: x[1], reverse=True)[:10]:
                print(f"   • {warranty}: {count} products")
    
    def get_product_recommendations(self, product_id: str, limit: int = 5) -> List[Dict]:
        """
        Get product recommendations based on similar attributes.
        
        Args:
            product_id (str): ID of the reference product
            limit (int): Number of recommendations
            
        Returns:
            List[Dict]: Recommended products
        """
        print(f"\n🎯 Finding recommendations for product ID: {product_id}")
        
        # Find the reference product
        reference_product = None
        for product in self.data:
            if product.get('id') == product_id:
                reference_product = product
                break
        
        if not reference_product:
            print(f"❌ Product with ID {product_id} not found")
            return []
        
        # Calculate similarity scores
        recommendations = []
        ref_attrs = set(reference_product.keys())
        
        for product in self.data:
            if product.get('id') == product_id:
                continue
            
            # Calculate similarity based on common attributes
            product_attrs = set(product.keys())
            common_attrs = ref_attrs.intersection(product_attrs)
            
            if not common_attrs:
                continue
            
            similarity_score = 0
            for attr in common_attrs:
                if attr == 'id':
                    continue
                
                ref_val = str(reference_product[attr]).lower()
                prod_val = str(product[attr]).lower()
                
                # Simple text similarity
                if ref_val == prod_val:
                    similarity_score += 2
                elif any(word in prod_val for word in ref_val.split() if len(word) > 2):
                    similarity_score += 1
            
            if similarity_score > 0:
                recommendations.append((similarity_score, product))
        
        # Sort by similarity and return top results
        recommendations.sort(reverse=True, key=lambda x: x[0])
        results = [product for score, product in recommendations[:limit]]
        
        print(f"✅ Found {len(results)} similar products")
        return results
    
    def export_analysis(self, filename: str = None):
        """Export analysis results to a file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ecommerce_analysis_{timestamp}.json"
        
        analysis_data = {
            'timestamp': datetime.now().isoformat(),
            'total_products': len(self.data),
            'data_structure': self.explore_data_structure(),
            'search_index_size': len(self.search_index)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analysis exported to {filename}")
    
    def interactive_query_interface(self):
        """Run an interactive command-line interface for querying data."""
        print("\n" + "="*60)
        print("🎮 INTERACTIVE QUERY INTERFACE")
        print("="*60)
        print("Commands:")
        print("  search <query>     - Search products")
        print("  filter <attr>=<value> - Filter by attribute")
        print("  recommend <id>     - Get recommendations")
        print("  stats              - Show data statistics")
        print("  categories         - Analyze categories")
        print("  pricing            - Analyze pricing/weights")
        print("  export             - Export analysis")
        print("  help               - Show this help")
        print("  quit               - Exit interface")
        print("-" * 60)
        
        while True:
            try:
                command = input("\n🔍 Enter command: ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("👋 Goodbye!")
                    break
                elif command == 'help':
                    self.interactive_query_interface()
                    break
                elif command == 'stats':
                    self.explore_data_structure()
                elif command == 'categories':
                    self.analyze_categories()
                elif command == 'pricing':
                    self.analyze_pricing_and_weights()
                elif command == 'export':
                    self.export_analysis()
                elif command.startswith('search '):
                    query = command[7:]
                    results = self.search_products(query, limit=5)
                    self._display_products(results)
                elif command.startswith('recommend '):
                    product_id = command[10:].strip()
                    results = self.get_product_recommendations(product_id, limit=3)
                    self._display_products(results)
                elif command.startswith('filter '):
                    # Simple filter parsing
                    filter_str = command[7:]
                    if '=' in filter_str:
                        attr, value = filter_str.split('=', 1)
                        filters = {attr.strip(): value.strip()}
                        results = self.filter_products(filters)
                        self._display_products(results[:5])
                    else:
                        print("❌ Invalid filter format. Use: filter attribute=value")
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def _display_products(self, products: List[Dict], max_display: int = 5):
        """Display products in a formatted way."""
        if not products:
            print("No products to display")
            return
        
        for i, product in enumerate(products[:max_display], 1):
            print(f"\n📦 Product {i}:")
            print(f"   ID: {product.get('id', 'N/A')}")
            
            # Display key attributes
            important_attrs = ['Type', 'Brand', 'Model Number', 'Model Name', 
                             'Weight', 'Sales Package', 'Features']
            
            for attr in important_attrs:
                if attr in product:
                    value = str(product[attr])
                    if len(value) > 80:
                        value = value[:77] + "..."
                    print(f"   {attr}: {value}")
            
            # Show total attributes
            print(f"   Total Attributes: {len(product)}")


def main():
    """Main function to run the E-Commerce Query Processor."""
    print("🛒 E-Commerce Data Query Processor & Explorer")
    print("=" * 50)
    
    # Initialize the processor
    processor = ECommerceQueryProcessor()
    
    # Load data
    data_file = "../data-set.json"  # Relative path to data file
    if not processor.load_data(data_file):
        print("Failed to load data. Please check the file path.")
        return
    
    # Run comprehensive analysis
    print("\n🚀 Starting comprehensive data analysis...")
    
    # 1. Explore data structure
    processor.explore_data_structure()
    
    # 2. Analyze categories
    processor.analyze_categories()
    
    # 3. Analyze pricing and weights
    processor.analyze_pricing_and_weights()
    
    # 4. Demonstrate search functionality
    print("\n" + "="*60)
    print("🔍 SEARCH DEMONSTRATION")
    print("="*60)
    
    sample_searches = ["vacuum cleaner", "bluetooth", "car", "LED", "waterproof"]
    for query in sample_searches:
        results = processor.search_products(query, limit=3)
        if results:
            print(f"\nTop results for '{query}':")
            processor._display_products(results, max_display=2)
    
    # 5. Demonstrate filtering
    print("\n" + "="*60)
    print("🎯 FILTER DEMONSTRATION")
    print("="*60)
    
    sample_filters = [
        {"Type": "Car Vacuum Cleaner"},
        {"Brand": "Portronics"},
    ]
    
    for filters in sample_filters:
        results = processor.filter_products(filters)
        if results:
            print(f"\nFiltered results for {filters}:")
            processor._display_products(results, max_display=2)
    
    # 6. Demonstrate recommendations
    print("\n" + "="*60)
    print("🎯 RECOMMENDATION DEMONSTRATION")
    print("="*60)
    
    # Get recommendations for first few products
    for i in range(1, 4):
        recommendations = processor.get_product_recommendations(str(i), limit=2)
        if recommendations:
            print(f"\nRecommendations for product ID {i}:")
            processor._display_products(recommendations, max_display=2)
    
    # 7. Export analysis
    processor.export_analysis()
    
    # 8. Start interactive interface
    print("\n🎮 Starting interactive interface...")
    processor.interactive_query_interface()


if __name__ == "__main__":
    # Set up Python environment for optimal performance
    import sys
    import os
    
    # Add current directory to path for imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()