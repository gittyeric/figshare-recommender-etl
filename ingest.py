import requests
import json

FILE_NAME = 'feed.xml'
API_URL = 'https://api.figshare.com/v2/institution/hrfeed/upload'
TOKEN = '86bbaa5d6d51fc0ae2f2defd3a474dac77ae27179ff6d04dd37e74c531bd6ed059eda584b41356337c362a259e482eb36a34825c805344e0600bb875a77444df'
headers = {"Authorization": "token " + TOKEN}
PAGE_SIZE = 100

def main():
    lastSeenId = ""

    while True:
        resp = sendRequest(API_URL + "", {}, "created")
        try:
            results = parseResponse(resp.content)
            print(json.dumps(results))

            #if len(results) == 0:
            #print("Done Ingesting!!!")
            #break


        except:
            print("Error occurred calling api!")
            break
        resp.raise_for_status()

def parseResponse(resp):
    result = json.loads(resp.content)
    return result

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
