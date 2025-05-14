from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bombay HC Scraper is working."

@app.route('/scrape')
def scrape():
    url = "https://bombayhighcourt.nic.in/displayboard.php?bhcpar=Y250PTMmb2xkdGltZT0xNzQ3MjAwMzczJmxvY2F0aW9uPUJvbWJheQ=="
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.select('#cardContainer .card')

    results = []
    for card in cards:
        values = [val.get_text(strip=True) for val in card.select('.card-item .value')]
        if values:
            results.append(values)

    return jsonify(results)
