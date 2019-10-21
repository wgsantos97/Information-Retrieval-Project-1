import json

# CLASSES


class JsonDataParse:
    def __init__(self, f):
        self.totalwords = 0  # Number of words in total
        self.population = 0  # Number of documents in this set
        self.min = 999999999
        self.max = 0
        self.avg = 0

        for line in f:
            self.population = self.population + 1
            d = json.loads(line)
            length = len(d["review_text"].split())
            self.totalwords = self.totalwords + length
            if(length > self.max):
                self.max = length
            if(length < self.min):
                self.min = length

        self.avg = self.totalwords/self.population

    def report(self, f):
        f.write("# JSON Stats")
        f.write("\n\n\tTotal Words: " + str(self.totalwords) + " words")
        f.write("\n\tDocument Population: " +
                str(self.population) + " documents")
        f.write("\n\tAverage Word Count: " +
                str(self.avg) + " words per document")
        f.write("\n\tMax Word Count: " + str(self.max) + " words")
        f.write("\n\tMin Word Count: " + str(self.min) + " words\n")

# MAIN


def main():
    fileTarget = "Results.md"
    fileRead = "Data/graphic_novel_reviews.json"
    path = "../"
    f = open(path + fileRead, 'r')
    jDP = JsonDataParse(f)
    f.close()
    f = open(fileTarget, 'w')
    jDP.report(f)
    f.close()


main()
