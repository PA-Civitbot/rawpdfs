from flask import Flask
from scripts.search import search_all_files_for_pattern
import json


app = Flask(__name__)


@app.route("/")
def homepage():
    return "Hello World to my <strong>homepage</strong>!"

@app.route("/search/<pattern>")
def searchpage(pattern):
    matches = search_all_files_for_pattern(pattern)
    return json.dumps(matches, indent=2)


if __name__ == "__main__":
     app.run(debug=True, use_reloader=True)
