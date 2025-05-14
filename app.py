from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/data")
def get_display_board():
    try:
        url = "https://bombayhighcourt.nic.in/displayboard.php?bhcpar=Y250PTMmb2xkdGltZT0xNzQ3MjAwMzczJmxvY2F0aW9uPUJvbWJheQ=="
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://bombayhighcourt.nic.in"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("#cardContainer .card")

        data = []
        for card in cards:
            values = [item.get_text(strip=True) for item in card.select(".card-item")]
            if len(values) >= 3:
                data.append({
                    "cr_no": values[0],
                    "sr_no": values[1],
                    "case_no": values[2],
                    "coram": values[3] if len(values) > 3 else "",
                    "kept_back": values[4] if len(values) > 4 else ""
                })

        return jsonify({"status": "success", "count": len(data), "results": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
