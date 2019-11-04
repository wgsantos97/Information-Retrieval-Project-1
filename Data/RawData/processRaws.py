import json

# This only ever needs to run once.


def main():
    startfile = "graphic_novels_raw.json"
    endfile = "../graphic_novels.json"
    f = open(startfile, 'r')
    data = dict()
    for line in f:
        #entry = dict()
        d = json.loads(line)
        key = d["book_id"]
        value = d["title"]
        data[key] = value
        #data.append(entry)
    f.close()

    f = open(endfile, 'w')
    json.dump(data, f)
    f.close()


main()
