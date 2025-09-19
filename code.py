from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

# Add this function to handle OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = app.make_response("")
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

@app.route('/code.py', methods=['GET', 'OPTIONS']) # Add 'OPTIONS' here
def fetch_html():
    url = request.args.get('url', '')
    
    # Validate URL
    if not url:
        return jsonify({
            'html': '',
            'size': '0 B',
            'error': 'No URL provided.'
        })
    
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({
            'html': '',
            'size': '0 B',
            'error': 'Invalid URL format. Please use http:// or https://'
        })
    
    try:
        # Fetch the content
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SourceViewer/1.0)'
        })
        response.raise_for_status()
        
        html_content = response.text
        
        res = jsonify({
            'html': html_content,
            'size': f"{len(html_content)} B",
            'error': None
        })
        # Add CORS headers to the main response
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res
        
    except Exception as e:
        res = jsonify({
            'html': '',
            'size': '0 B',
            'error': f'Failed to fetch content: {str(e)}'
        })
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
