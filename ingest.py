import api
import bookmark as bmark
import kafka_output as outputter
import rec_formatter


def main():

    bookmark = bmark.load()

    while True:
        articles = api.fetch_next_articles(bookmark)

        if len(articles) == 0:
            print("All done for now!")
            break
        else:
            bookmark.update_from(articles)
            save(articles)
            print("Saved up to " + bookmark.date_str() + " (page " + str(bookmark.page()) + ")")


def save(articles):
    rec_messages = rec_formatter.to_rec_messages(articles)
    # print(json.dumps(rec_messages, indent=2))
    outputter.save_messages(rec_messages)


if __name__ == '__main__':
    main()
