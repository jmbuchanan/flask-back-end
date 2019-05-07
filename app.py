from flask import Flask
import json

from repository import Repository


app = Flask(__name__)

@app.route('/')
def index():
    return '/auctions'


@app.route('/auctions')
def api():

    repo = Repository()
    results = repo.get_historical_prices()
    json_results = []

    for result in results:
        json_results.append(result.__dict__)

    return json.dumps(json_results)


if __name__ == "__main__":
    app.run()
