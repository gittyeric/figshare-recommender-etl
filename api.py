import json
import multiprocessing
import requests
from multiprocessing.pool import ThreadPool

multiprocessing.freeze_support()

API_URL = 'https://api.figshare.com/v2/'
TOKEN = '86bbaa5d6d51fc0ae2f2defd3a474dac77ae27179ff6d04dd37e74c531bd6ed059eda584b41356337c362a259e482eb36a34825c805344e0600bb875a77444df'
HEADERS = {"Authorization": "token " + TOKEN}
PAGE_SIZE = 100
REQUEST_POOL = ThreadPool(10)  # Never more than REQUEST_POOL API calls at once


def fetch_next_articles(bmark):
    try:
        resp = _send_request(API_URL + "articles", {}, bmark, "published_date")
        ids = _parse_id_list_from_response(resp)
        articles = _fetch_articles_by_ids(ids)

        # Remove erroneous responses
        actual_articles = [article for article in articles if article is not None]
        return actual_articles
    except Exception as e:
        print("Error occurred calling api! " + str(e))
        exit(1)


def _fetch_articles_by_ids(ids):
    # Get articles from article_ids in parallel
    return REQUEST_POOL.map(_fetch_article_by_id, ids)


def _fetch_article_by_id(id):
    try:
        resp = _send_request(API_URL + "articles/" + str(id), {})
        return _parse_article_from_response(resp)
    except Exception as e:
        print(e)
        return None


def _parse_article_from_response(resp):
    return json.loads(resp.text)


def _parse_id_list_from_response(resp):
    articles = json.loads(resp.text)
    return map(lambda article: article["id"], articles)


def _send_request(api, params, bmark=None, order_field="publication_date", since_field="published_since"):
    if order_field is not None:
        params["ordering"] = order_field
        params["order_direction"] = "asc"

    if bmark is not None:
        params = _add_paging_params(params, bmark, since_field)

    resp = requests.get(api, params, headers=HEADERS)
    resp.raise_for_status()
    return resp


def _add_paging_params(params, bmark, since_field):
    params["page"] = bmark.page()
    params["page_size"] = PAGE_SIZE
    if bmark.date_str is not None:
        params[since_field] = bmark.date_str()

    return params
