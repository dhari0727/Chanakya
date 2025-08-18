import os
import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    """Homepage with centered search bar"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search results page"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('index'))
    
    # Load mock search results
    try:
        with open('static/data/mock_results.json', 'r') as f:
            all_results = json.load(f)
    except FileNotFoundError:
        all_results = []
    
    # Simple pagination
    results_per_page = 10
    start_idx = (page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    
    # Filter results based on query (simple matching)
    filtered_results = []
    for result in all_results:
        if query.lower() in result['title'].lower() or query.lower() in result['snippet'].lower():
            filtered_results.append(result)
    
    # If no specific matches, return some general results
    if not filtered_results:
        filtered_results = all_results[:20]  # Return first 20 as general results
    
    paginated_results = filtered_results[start_idx:end_idx]
    total_results = len(filtered_results)
    
    # Calculate pagination info
    total_pages = (total_results + results_per_page - 1) // results_per_page
    
    return render_template('search.html', 
                         query=query, 
                         results=paginated_results,
                         page=page,
                         total_pages=total_pages,
                         total_results=total_results,
                         results_per_page=results_per_page)

@app.route('/api/suggestions')
def get_suggestions():
    """API endpoint for search suggestions"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify([])
    
    try:
        with open('static/data/suggestions.json', 'r') as f:
            suggestions = json.load(f)
    except FileNotFoundError:
        suggestions = []
    
    # Filter suggestions based on query
    filtered_suggestions = [s for s in suggestions if query in s.lower()]
    
    return jsonify(filtered_suggestions[:8])  # Return max 8 suggestions

@app.route('/lucky')
def feeling_lucky():
    """I'm Feeling Lucky functionality"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('index'))
    
    # Load first result and redirect to its URL
    try:
        with open('static/data/mock_results.json', 'r') as f:
            results = json.load(f)
        
        if results:
            # For demo purposes, redirect to search page with first result
            return redirect(url_for('search', q=query))
    except FileNotFoundError:
        pass
    
    return redirect(url_for('search', q=query))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
