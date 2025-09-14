#!/usr/bin/env python3
"""
E-Commerce Web Interface
========================

A simple web interface for the e-commerce query processor using Flask.
This creates a basic UI that you can access in your browser.
"""

from flask import Flask, render_template, request, jsonify
import json
import re
from collections import defaultdict, Counter

app = Flask(__name__)

class WebECommerceParser:
    """Web-enabled e-commerce parser."""
    
    def __init__(self):
        self.data = []
        self.search_index = defaultdict(set)
        # Try different possible paths for the data file
        import os
        possible_paths = [
            "../data-set.json",
            "../../data-set.json", 
            r"c:\Users\Asus\Documents\knit-intern\data-set.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.load_data(path)
                break
        else:
            print("❌ Could not find data-set.json file")
    
    def load_data(self, file_path: str):
        """Load product data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self._build_search_index()
            print(f"✅ Loaded {len(self.data)} products for web interface")
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
    
    def _build_search_index(self):
        """Build search index."""
        for idx, product in enumerate(self.data):
            for key, value in product.items():
                if isinstance(value, str):
                    words = re.findall(r'\b\w+\b', value.lower())
                    for word in words:
                        self.search_index[word].add(idx)
    
    def search(self, query: str, limit: int = 20):
        """Search for products."""
        query_words = re.findall(r'\b\w+\b', query.lower())
        if not query_words:
            return []
        
        matching_indices = set()
        for word in query_words:
            if word in self.search_index:
                matching_indices.update(self.search_index[word])
        
        scored_results = []
        for idx in matching_indices:
            product = self.data[idx]
            score = 0
            
            for key, value in product.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for word in query_words:
                        score += value_lower.count(word)
            
            scored_results.append((score, product))
        
        scored_results.sort(reverse=True, key=lambda x: x[0])
        return [product for score, product in scored_results[:limit]]
    
    def get_stats(self):
        """Get basic statistics."""
        all_attributes = set()
        attribute_counts = Counter()
        type_counts = Counter()
        brand_counts = Counter()
        
        for product in self.data:
            product_attrs = set(product.keys())
            all_attributes.update(product_attrs)
            attribute_counts.update(product_attrs)
            
            if 'Type' in product:
                type_counts[product['Type']] += 1
            if 'Brand' in product:
                brand_counts[product['Brand']] += 1
        
        return {
            'total_products': len(self.data),
            'unique_attributes': len(all_attributes),
            'top_attributes': dict(attribute_counts.most_common(10)),
            'top_types': dict(type_counts.most_common(10)),
            'top_brands': dict(brand_counts.most_common(10))
        }

# Initialize the parser
parser = WebECommerceParser()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/search')
def api_search():
    """Search API endpoint."""
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return jsonify({'results': [], 'count': 0})
    
    results = parser.search(query, limit)
    return jsonify({
        'results': results,
        'count': len(results),
        'query': query
    })

@app.route('/api/stats')
def api_stats():
    """Statistics API endpoint."""
    stats = parser.get_stats()
    return jsonify(stats)

@app.route('/api/product/<product_id>')
def api_product(product_id):
    """Get specific product by ID."""
    for product in parser.data:
        if product.get('id') == product_id:
            return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    print("🌐 Starting E-Commerce Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
