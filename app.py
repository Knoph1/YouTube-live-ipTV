import re
import requests

from flask import Flask, request
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})

class BaseM3URetrievalException(Exception):
    pass


class M3ULinkNotFoundException(BaseM3URetrievalException):
    pass


class M3URetrievalHTTPException(BaseM3URetrievalException):
    pass





if __name__ == "__main__":
    app.run()