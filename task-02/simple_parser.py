"""
Simple E-Commerce Data Parser (No External Dependencies)
======================================================

A lightweight e-commerce data processor using only Python standard library.
Perfect for understanding the core concepts without external dependencies.
"""

import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional


class SimpleECommerceParser:
    
    def __init__(self, data_file: str = None):
        """Initialize the parser with optional data file."""
        self.data = []
        self.search_index = defaultdict(set)
        
        if data_file:
            self.load_data(data_file)
    
    def load_data(self, file_path: str) -> bool:
        """Load product data from JSON file."""
        try:
            print(f"📂 Loading data from {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            
            self._build_search_index()
            print(f"✅ Successfully loaded {len(self.data)} products")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False
    
    def _build_search_index(self):
        """Build an inverted index for fast text searching."""
        print("🔨 Building search index...")
        for idx, product in enumerate(self.data):
            for key, value in product.items():
                if isinstance(value, str):
                    words = re.findall(r'\b\w+\b', value.lower())
                    for word in words:
                        self.search_index[word].add(idx)
        print(f"✅ Search index built with {len(self.search_index)} terms")
    
    def basic_stats(self):
        """Show basic statistics about the dataset."""
        print("\n" + "="*50)
        print("📊 BASIC STATISTICS")
        print("="*50)
        
        if not self.data:
            print("❌ No data loaded")
            return
        
        print(f"📈 Total Products: {len(self.data)}")
        
        # Count all attributes
        all_attributes = set()
        attribute_counts = Counter()
        
        for product in self.data:
            product_attrs = set(product.keys())
            all_attributes.update(product_attrs)
            attribute_counts.update(product_attrs)
        
        print(f"📈 Unique Attributes: {len(all_attributes)}")
        
        # Most common attributes
        print("\n🔝 Top 10 Most Common Attributes:")
        for attr, count in attribute_counts.most_common(10):
            percentage = (count / len(self.data)) * 100
            print(f"   • {attr}: {count} ({percentage:.1f}%)")
        
        return {
            'total_products': len(self.data),
            'unique_attributes': len(all_attributes),
            'top_attributes': dict(attribute_counts.most_common(10))
        }
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for products using text query."""
        print(f"\n🔍 Searching for: '{query}'")
        
        query_words = re.findall(r'\b\w+\b', query.lower())
        if not query_words:
            return []
        
        # Find matching products
        matching_indices = set()
        for word in query_words:
            if word in self.search_index:
                matching_indices.update(self.search_index[word])
        
        # Score and sort results
        scored_results = []
        for idx in matching_indices:
            product = self.data[idx]
            score = 0
            
            # Calculate relevance score
            for key, value in product.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for word in query_words:
                        score += value_lower.count(word)
            
            scored_results.append((score, product))
        
        # Sort by score and return top results
        scored_results.sort(reverse=True, key=lambda x: x[0])
        results = [product for score, product in scored_results[:limit]]
        
        print(f"✅ Found {len(results)} matching products")
        return results
    
    def filter_by_attribute(self, attribute: str, value: str) -> List[Dict]:
        """Filter products by a specific attribute value."""
        print(f"\n🎯 Filtering by {attribute} = {value}")
        
        results = []
        for product in self.data:
            if attribute in product:
                product_value = str(product[attribute]).lower()
                if value.lower() in product_value:
                    results.append(product)
        
        print(f"✅ Found {len(results)} matching products")
        return results
    
    def analyze_categories(self):
        """Analyze product categories and types."""
        print("\n" + "="*50)
        print("📂 CATEGORY ANALYSIS")
        print("="*50)
        
        # Analyze product types
        type_counter = Counter()
        brand_counter = Counter()
        
        for product in self.data:
            if 'Type' in product:
                type_counter[product['Type']] += 1
            if 'Brand' in product:
                brand_counter[product['Brand']] += 1
        
        if type_counter:
            print("🏷️  Top Product Types:")
            for product_type, count in type_counter.most_common(10):
                print(f"   • {product_type}: {count} products")
        
        if brand_counter:
            print("\n🏢 Top Brands:")
            for brand, count in brand_counter.most_common(10):
                print(f"   • {brand}: {count} products")
        
        return {
            'types': dict(type_counter.most_common(10)),
            'brands': dict(brand_counter.most_common(10))
        }
    
    def find_similar_products(self, product_id: str, limit: int = 5) -> List[Dict]:
        """Find similar products based on shared attributes."""
        print(f"\n🎯 Finding similar products to ID: {product_id}")
        
        # Find reference product
        reference = None
        for product in self.data:
            if product.get('id') == product_id:
                reference = product
                break
        
        if not reference:
            print(f"❌ Product with ID {product_id} not found")
            return []
        
        # Calculate similarity scores
        similarities = []
        ref_attrs = set(reference.keys())
        
        for product in self.data:
            if product.get('id') == product_id:
                continue
            
            product_attrs = set(product.keys())
            common_attrs = ref_attrs.intersection(product_attrs)
            
            similarity_score = 0
            for attr in common_attrs:
                if attr == 'id':
                    continue
                
                ref_val = str(reference[attr]).lower()
                prod_val = str(product[attr]).lower()
                
                if ref_val == prod_val:
                    similarity_score += 2
                elif any(word in prod_val for word in ref_val.split() if len(word) > 2):
                    similarity_score += 1
            
            if similarity_score > 0:
                similarities.append((similarity_score, product))
        
        # Sort and return top results
        similarities.sort(reverse=True, key=lambda x: x[0])
        results = [product for score, product in similarities[:limit]]
        
        print(f"✅ Found {len(results)} similar products")
        return results
    
    def export_summary(self, filename: str = "summary.json"):
        """Export a summary of the analysis."""
        summary = {
            'basic_stats': self.basic_stats(),
            'categories': self.analyze_categories(),
            'sample_products': self.data[:5]  # First 5 products as examples
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Summary exported to {filename}")
    
    def display_product(self, product: Dict, detailed: bool = False):
        """Display a single product in a formatted way."""
        print(f"\n📦 Product ID: {product.get('id', 'N/A')}")
        
        # Key attributes to always show
        key_attrs = ['Type', 'Brand', 'Model Number', 'Model Name', 
                    'Weight', 'Sales Package']
        
        for attr in key_attrs:
            if attr in product:
                value = str(product[attr])
                if len(value) > 60:
                    value = value[:57] + "..."
                print(f"   {attr}: {value}")
        
        if detailed:
            print("   All Attributes:")
            for key, value in product.items():
                if key not in key_attrs and key != 'id':
                    value_str = str(value)
                    if len(value_str) > 50:
                        value_str = value_str[:47] + "..."
                    print(f"     • {key}: {value_str}")
        
        print(f"   Total Attributes: {len(product)}")
    
    def interactive_mode(self):
        """Run interactive command mode."""
        print("\n" + "="*50)
        print("🎮 INTERACTIVE MODE")
        print("="*50)
        print("Commands:")
        print("  search <query>     - Search products")
        print("  filter <attr> <value> - Filter by attribute")
        print("  similar <id>       - Find similar products")
        print("  stats              - Show basic statistics")
        print("  categories         - Analyze categories")
        print("  export             - Export summary")
        print("  quit               - Exit")
        print("-" * 50)
        
        while True:
            try:
                command = input("\n🔍 Command: ").strip()
                
                if command.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif command.lower() == 'stats':
                    self.basic_stats()
                elif command.lower() == 'categories':
                    self.analyze_categories()
                elif command.lower() == 'export':
                    self.export_summary()
                elif command.startswith('search '):
                    query = command[7:]
                    results = self.search(query, limit=3)
                    for product in results:
                        self.display_product(product)
                elif command.startswith('filter '):
                    parts = command[7:].split(' ', 1)
                    if len(parts) == 2:
                        attr, value = parts
                        results = self.filter_by_attribute(attr, value)
                        for product in results[:3]:
                            self.display_product(product)
                    else:
                        print("❌ Usage: filter <attribute> <value>")
                elif command.startswith('similar '):
                    product_id = command[8:].strip()
                    results = self.find_similar_products(product_id, limit=3)
                    for product in results:
                        self.display_product(product)
                else:
                    print("❌ Unknown command. Available: search, filter, similar, stats, categories, export, quit")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def demo_all_features():
    """Demonstrate all features of the parser."""
    print("🛒 E-Commerce Simple Parser Demo")
    print("=" * 40)
    
    # Initialize parser
    parser = SimpleECommerceParser("./data-set.json")
    
    if not parser.data:
        print("Failed to load data!")
        return
    
    # Run demonstrations
    parser.basic_stats()
    parser.analyze_categories()
    
    # Search demos
    search_queries = ["vacuum", "bluetooth", "car", "LED"]
    for query in search_queries:
        results = parser.search(query, limit=2)
        if results:
            print(f"\n🔍 Search results for '{query}':")
            for product in results:
                parser.display_product(product)
    
    # Filter demo
    results = parser.filter_by_attribute("Type", "Car Vacuum Cleaner")
    if results:
        print(f"\n🎯 Filter results:")
        parser.display_product(results[0], detailed=True)
    
    # Similarity demo
    similar = parser.find_similar_products("2", limit=2)
    if similar:
        print(f"\n🎯 Similar products:")
        for product in similar:
            parser.display_product(product)
    
    # Export summary
    parser.export_summary()
    
    # Start interactive mode
    print("\n🚀 Starting interactive mode...")
    parser.interactive_mode()


if __name__ == "__main__":
    demo_all_features()
