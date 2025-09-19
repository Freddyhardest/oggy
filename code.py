from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/code.py')
def fetch_html():
    url = request.args.get('url', '')
    
    # Validate URL
    if not url:
        return jsonify({
            'html': '',
            'size': '0 B',
            'time': '0.00',
            'error': 'No URL provided.'
        })
    
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({
            'html': '',
            'size': '0 B',
            'time': '0.00',
            'error': 'Invalid URL format. Please use http:// or https://'
        })
    
    try:
        # Fetch the content
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; SourceViewer/1.0)'
        })
        response.raise_for_status()
        
        html_content = response.text
        
        return jsonify({
            'html': html_content,
            'size': f"{len(html_content)} B",
            'time': "0.00", # You'd need to add timing logic
            'error': None
        })
        
    except Exception as e:
        return jsonify({
            'html': '',
            'size': '0 B',
            'time': '0.00',
            'error': f'Failed to fetch content: {str(e)}'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
