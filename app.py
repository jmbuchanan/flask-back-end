from flask import Flask
import json

from repository import Repository


app = Flask(__name__)

@app.route('/auctions')
def get_price_over_time():
    "Returns a list of PriceOverTime objects as JSON."

    repo = Repository()
    results = repo.get_historical_prices()
    json_results = []

    #__dict__ attribute returns object attributes as dict
    for result in results:
        json_results.append(result.__dict__)

    return json.dumps(json_results)


if __name__ == "__main__":
    app.run()
