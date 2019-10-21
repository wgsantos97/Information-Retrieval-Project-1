import json

# CLASSES
class DocumentData:
    def __init__(self, f):
        self.amount = 0
        self.min = 0
        self.max = 0
        self.avg = 0


# MAIN
def main():
    fileTarget = "Results.txt"
    fileRead = "Data/graphic_novel_reviews.json"
    path = "../" + fileRead
    f = open(path, 'r')


main()
