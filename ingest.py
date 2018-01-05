import requests
import json
import os

API_URL = 'https://api.figshare.com/v2/'
TOKEN = '86bbaa5d6d51fc0ae2f2defd3a474dac77ae27179ff6d04dd37e74c531bd6ed059eda584b41356337c362a259e482eb36a34825c805344e0600bb875a77444df'
headers = {"Authorization": "token " + TOKEN}
PAGE_SIZE = 2

def main():
    bookmark = loadBookmark()

    while True:
        bookmark = fetchNextArticles(bookmark)

        if bookmark["article"] is None:
            break


def loadBookmark():
    if os.path.isfile("bookmark.json"):
        with open("bookmark.json", "r") as file:
            return json.loads(file.read())

    return {"article": False}

def saveBookmark(bookmark):
    with open("bookmark.json", "w") as file:
        file.write(json.dumps(bookmark))

def fetchNextArticles(bookmark):
    if bookmark["article"] is None:
        return bookmark

    page = 1
    if bookmark["article"]:
        page = bookmark["article"]

    resp = sendRequest(API_URL + "articles", {}, page, "published_date")
    try:
        resp.raise_for_status()
        ids = parseIdListFromResponse(resp)
        print(json.dumps(ids, indent=2))

        # 3732171
        # if len(ids) == 0:
        # print("Done Ingesting!!!")
        bookmark["article"] = None

        #bookmark["article"] = ids[-1]["published_date"]
    except Exception as e:
        print("Error occurred calling api! " + str(e))
        exit(1)

    return bookmark

def parseIdListFromResponse(resp):
    list = json.loads(resp.text)
    ids = []
    for el in list:
        ids += el.id
    return ids

def sendRequest(api, params, page, dateField):
    params["ordering"] = dateField
    params["order_direction"] = "asc"
    params = addPagingParams(params, page)

    return requests.get(api, params, headers=headers)

def addPagingParams(params, page):
    params["page"] = page
    params["page_size"] = PAGE_SIZE
    return params

if __name__ == '__main__':
    main()
