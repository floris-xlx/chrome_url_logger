from flask import Flask, request
from flask_cors import CORS
import datetime
import json
import tldextract
import os

app = Flask(__name__)

# Enable CORS for your specific Chrome extension
CORS(app, resources={r"/log": {"origins": "chrome-extension://knkkkiahkkfafonpepebnfjpoejdjcpe"}})

# Path to the JSON file where URLs will be stored
json_file = 'visited_urls.json'

def get_visited_urls():
    """Retrieve the list of visited URLs from the JSON file."""
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    return []

def save_visited_urls(urls):
    """Save the list of visited URLs to the JSON file."""
    with open(json_file, 'w') as file:
        json.dump(urls, file, indent=4)

@app.route('/log', methods=['POST'])
def log_url():
    data = request.json
    if 'url' in data:
        url = data['url']
        
        # Extract domain and TLD using tldextract
        extracted = tldextract.extract(url)
        host = extracted.subdomain + '.' + extracted.domain + '.' + extracted.suffix if extracted.subdomain else extracted.domain + '.' + extracted.suffix
        domain = extracted.domain
        tld = extracted.suffix
        timestamp = int(datetime.datetime.now().timestamp())

        # Prepare the URL data
        url_data = {
            'host': host,
            'domain': domain,
            'tld': tld,
            'time': timestamp,
            'full_request': data  # Store the full request data
        }

        # Get the existing list of URLs
        visited_urls = get_visited_urls()

        # Check for duplicates based on the full_request.url only
        is_duplicate = any(
            entry['full_request']['url'] == url_data['full_request']['url']
            for entry in visited_urls
        )

        if not is_duplicate:
            visited_urls.append(url_data)
            save_visited_urls(visited_urls)  # Save the updated list to the JSON file

    return '', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
