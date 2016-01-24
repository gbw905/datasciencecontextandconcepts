import sys
import json
import re
import unicodedata

def hw():
    print 'Start Run ' + sys.argv[0]

def gw():
    print 'End Run ' + sys.argv[0]

def main():
    #hw()
    tweet_file = open(sys.argv[1])

    #extract hashtags from all tweets into a list
    tagList = []
    for line in tweet_file:
        d = json.loads(line)
        if d.has_key("entities") and d["entities"] is not None:
            if d["entities"]["hashtags"] is not None and len(d["entities"]["hashtags"]) > 0:
                for tagItem in d["entities"]["hashtags"]:
                    tagList.append(tagItem["text"].lower())

    #count occurrences of each unique hashtag
    tagDict = {}
    for tag in tagList:
        if tag != "":
            try:
                tagDict[tag] += 1
            except(KeyError):
                tagDict[tag] = 1

    #extract dictionary to list and sort descending by frequency of occurence
    toptags = sorted(tagDict.iteritems(), key=lambda x: x[1], reverse=True)

    #print the first ten entries on the sorted dictionary extract
    for idx in xrange(0,10):
        print toptags[idx][0], toptags[idx][1]

    #gw()

if __name__ == '__main__':
    main()

