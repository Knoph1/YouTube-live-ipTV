import re
import requests

from flask import Flask, request
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})




if __name__ == "__main__":
    app.run()