import json

def to_rec_messages(articles):
    messages = []

    for article in articles:
        aid = article["id"]
        for file in article["files"]:
            messages.append(to_tsv(["AHasFile", aid, file["id"]]))
        for author in article["authors"]:
            messages.append(to_tsv(["AuthoredA", author["id"], aid]))
        for cat in article["categories"]:
            messages.append(to_tsv(["AHasCat", aid, cat["id"]]))
        for tag in article["tags"]:
            messages.append(to_tsv(["AHasTag", aid, tag]))
        for ref in article["references"]:
            messages.append(to_tsv(["ARefsA", aid, ref]))

        if len(article["references"]) > 0:
            print(json.dumps(article["references"], indent=2))

        messages.append(to_tsv(["GroupHasA", article["group_id"], aid]))

    return messages

def to_tsv(params):
    tsv = ""
    for param in params:
        paramStr = str(param)
        if "\t" in paramStr:
            print("Cannot include tabbed param in TSV: " + json.dumps(params))
            exit(1)
        tsv += paramStr + "\t"

    return tsv[:-2]
