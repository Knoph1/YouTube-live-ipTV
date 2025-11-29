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


@cache.memoize(timeout=6 * 3600)
def get_m3u(url: str) -> str:
    """
    Get m3u contents from youtube video.
    Extracts m3u remote url from youtube video page and then retrieves its contents.
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise M3URetrievalHTTPException(
            f"Got error code: {resp.status_code} when retrieving yt video: {url}"
        )
    pattern = r"https?://[^\s\"'<>]+\.m3u8\b"
    match = re.search(pattern, resp.text)
    if not match:
        raise M3ULinkNotFoundException(f"Unable to find m3u url from yt video: {url}")
    m3u_url = match.group()
    m3u_content = requests.get(m3u_url)
    if resp.status_code != 200:
        raise M3URetrievalHTTPException(
            f"Got error code: {resp.status_code} when retrieving m3u content: {url}"
        )
    return m3u_content.text


@app.route("/")
def index() -> str:
    # TODO
    return "Hello world!"


def make_m3u_resp_from_url(url: str):
    try:
        return get_m3u(url)
    except M3ULinkNotFoundException as e:
        return f"Error: {e}", 404
    except BaseM3URetrievalException as e:
        return f"Error: {e}", 500


@app.route("/watch")
def make_m3u_from_yt_video():
    id = request.args.get("v")
    if not id:
        return "Error: Video ID not specified", 400
    return make_m3u_resp_from_url(f"https://youtube.com/watch?v={id}")


@app.route("/@<name>")
def make_m3u_from_channel_name(name: str):
    return make_m3u_resp_from_url(f"https://youtube.com/@{name}/live")


if __name__ == "__main__":
    app.run()