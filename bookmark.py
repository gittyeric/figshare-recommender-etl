import datetime
import json
import os
from datetime import datetime as dt

FIGSHARE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class DatePlumbing:

    def str_to_date(self, date_str):
        return dt.strptime(date_str, FIGSHARE_FORMAT)

    def date_to_str(self, dtime):
        return dtime.strftime(FIGSHARE_FORMAT)

    def article_to_date_str(self, article):
        return article["published_date"]


def load(date_plumbing=DatePlumbing()):
    if os.path.isfile("bookmark.json"):
        with open("bookmark.json", "r") as file:
            jsoned = json.loads(file.read())
            return BookMark(jsoned["page"], jsoned["date"], date_plumbing)

    return BookMark()


class BookMark:

    def __init__(self, page=1, date_str=None, date_plumbing=DatePlumbing()):
        self._page = page
        self._date_str = date_str
        self._dates = date_plumbing

    def page(self):
        return self._page

    def date_str(self):
        return self._date_str

    def update_from(self, newest_articles):
        newest_date_str = self._dates.article_to_date_str(newest_articles[-1])
        newest_date = self._dates.str_to_date(newest_date_str)
        newest_minus_1 = newest_date - datetime.timedelta(seconds=1)

        if self._date_str is None:
            self._page = 1
            self._date_str = self._dates.date_to_str(newest_minus_1)
        else:
            cur_page_date = self._dates.str_to_date(self._date_str)
            if newest_minus_1 == cur_page_date:
                self._page += 1
            else:
                self._page = 1
                self._date_str = self._dates.date_to_str(newest_minus_1)

        self._save()

    def _save(self):
        with open("bookmark.json", "w") as file:
            jsoned = json.dumps({"page": self._page, "date": self._date_str})
            file.write(jsoned)
