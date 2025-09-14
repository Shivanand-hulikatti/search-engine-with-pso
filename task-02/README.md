# E-Commerce Query Processor & Data Explorer

A comprehensive Python-based e-commerce data analysis tool that provides powerful querying, filtering, and exploration capabilities for product datasets.

## 🚀 Features

### Core Functionality
- **Data Loading & Processing**: Efficiently loads and processes large JSON datasets
- **Text Search**: Fast full-text search with relevance scoring
- **Advanced Filtering**: Filter products by attributes with range and text matching
- **Product Recommendations**: Find similar products based on shared attributes
- **Statistical Analysis**: Comprehensive dataset statistics and insights
- **Category Analysis**: Analyze product types, brands, and features

### User Interfaces
1. **Command Line Interface**: Interactive terminal-based querying
2. **Web Interface**: Modern, responsive web UI for easy browsing
3. **Simple Parser**: Lightweight version with no external dependencies

### Technical Features
- **Search Index**: Inverted index for fast text searching
- **Data Export**: Export analysis results to JSON
- **Error Handling**: Robust error handling and validation
- **Performance Optimized**: Efficient data structures and algorithms

## 📁 Project Structure

```
task-02/
├── main.py              # Comprehensive query processor with pandas/numpy
├── simple_parser.py     # Lightweight parser (no dependencies)
├── web_app.py          # Flask web application
├── templates/
│   └── index.html      # Web interface template
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Installation & Setup

### Option 1: Full Version (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run comprehensive analyzer
python main.py

# Or run web interface
python web_app.py
# Then open: http://localhost:5000
```

### Option 2: Lightweight Version (No Dependencies)
```bash
# Run simple parser (uses only Python standard library)
python simple_parser.py
```

## 📊 Dataset Overview

The tool analyzes an e-commerce dataset with:
- **21,176 products** across multiple categories
- **3,249 unique attributes** describing various product features
- **Diverse categories**: Electronics, appliances, accessories, supplements, etc.
- **Rich metadata**: Weights, dimensions, warranties, features, specifications

### Top Product Categories
- Home Appliances (Refrigerators, Washing Machines)
- Electronics (Laptops, Gaming Equipment, Audio)
- Accessories (Backpacks, Belts, Car Accessories)
- Health & Nutrition (Supplements, Fitness Equipment)
- Automotive (Car Vacuum Cleaners, LED Lights)

## 🔍 Usage Examples

### Command Line Interface
```python
# Search for products
search bluetooth speaker

# Filter by attributes
filter Type=Car Vacuum Cleaner

# Get recommendations
recommend 123

# View statistics
stats

# Analyze categories
categories
```

### Python API Usage
```python
from main import ECommerceQueryProcessor

# Initialize processor
processor = ECommerceQueryProcessor("data-set.json")

# Search products
results = processor.search_products("bluetooth speaker", limit=10)

# Filter products
filtered = processor.filter_products({"Type": "Gaming Laptop"})

# Get recommendations
similar = processor.get_product_recommendations("123", limit=5)

# Get statistics
stats = processor.explore_data_structure()
```

### Web Interface Features
- **Real-time Search**: Instant search results with relevance scoring
- **Interactive Statistics**: View dataset statistics and distributions
- **Responsive Design**: Works on desktop and mobile devices
- **Product Cards**: Clean, organized display of product information

## 🎯 Key Capabilities

### 1. Search & Discovery
- Full-text search across all product attributes
- Relevance-based ranking
- Support for multi-word queries
- Search result highlighting

### 2. Data Analysis
- Attribute frequency analysis
- Brand and category distribution
- Weight and dimension statistics
- Warranty analysis

### 3. Product Intelligence
- Similarity-based recommendations
- Feature extraction and analysis
- Category-based grouping
- Trend identification

### 4. Export & Integration
- JSON export of analysis results
- REST API endpoints for integration
- Structured data output
- Batch processing support

## 🛠️ Technical Architecture

### Core Components
1. **Data Loader**: Handles JSON parsing and validation
2. **Search Engine**: Inverted index with TF-IDF-like scoring
3. **Filter Engine**: Multi-criteria filtering with type checking
4. **Recommendation Engine**: Similarity calculation based on shared attributes
5. **Statistics Engine**: Comprehensive data analysis and insights

### Performance Features
- **Lazy Loading**: Load data only when needed
- **Indexed Search**: O(1) lookup for search terms
- **Cached Results**: Avoid redundant calculations
- **Memory Efficient**: Process large datasets without memory issues

## 📈 Use Cases

### Business Intelligence
- Market analysis and trend identification
- Inventory optimization
- Product categorization
- Competitive analysis

### E-commerce Applications
- Product search and discovery
- Recommendation systems
- Inventory management
- Customer analytics

### Data Science Projects
- Feature engineering for ML models
- Data exploration and visualization
- Pattern recognition
- Anomaly detection

## 🚀 Future Enhancements

### Planned Features
- **Machine Learning Integration**: Product classification and clustering
- **Advanced Analytics**: Price analysis, sales prediction
- **Real-time Updates**: Live data synchronization
- **API Endpoints**: RESTful API for external integration
- **Database Support**: PostgreSQL, MongoDB integration
- **Visualization**: Charts, graphs, and interactive plots

### Scalability Improvements
- **Distributed Processing**: Handle larger datasets
- **Caching Layer**: Redis integration for performance
- **Search Optimization**: Elasticsearch integration
- **Microservices**: Containerized deployment

## 🤝 Contributing

This is a hobby project that demonstrates:
- **Data Engineering**: Efficient data processing and indexing
- **Software Architecture**: Clean, modular design patterns
- **User Experience**: Multiple interface options for different use cases
- **Performance Optimization**: Fast search and analysis capabilities

## 📝 License

This project is for educational and hobby purposes. Feel free to use and modify as needed.

## 🎉 Hobby Project Highlights

This project showcases several important concepts:

1. **Full-Stack Development**: Backend data processing + Frontend web interface
2. **Data Engineering**: Efficient data structures and algorithms
3. **API Design**: Clean, RESTful endpoints
4. **User Experience**: Multiple interfaces for different users
5. **Performance**: Optimized for large datasets
6. **Modularity**: Easy to extend and customize

Perfect for portfolio demonstrations and learning advanced Python concepts!
