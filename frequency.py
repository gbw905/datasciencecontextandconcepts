import sys
import json
import re
import unicodedata

def hw():
    print 'Start Run ' + sys.argv[0]

def gw():
    print 'End Run ' + sys.argv[0]

def lines(fp):
    print str(len(fp.readlines()))

def mkNormal(iText):
    #oText = iText.strip()
    return unicodedata.normalize("NFKD", unicode(iText.lower().strip()))

def main():
    #hw()
    tweet_file = open(sys.argv[1])

    tweets = []
    for line in tweet_file:
        d = json.loads(line)
        #if "lang" in d.keys() and "text" in d.keys():
        #    if d["lang"].startswith("en"):
        if "text" in d.keys():
            tweets.append(d["text"])

    termList = []
    termDict = {}
    for tweet in tweets:
        encoded_tweet = tweet.encode("utf-8")
        words = encoded_tweet.split()
        for word in words: #remove words that cannot be a sentiment
            if word.startswith("RT") or word.startswith("www") or word.startswith("http"):
                words.remove(word)
        unwanted = re.compile('[^A-Za-z]+') #remove characters not used in English text
        words = [unwanted.sub("", word) for word in words]
        for word in words:
            termList.append(mkNormal(word)) #correct for accents and capitalization

    Cnt = len(termList)
    for term in termList:
        if term != "":
            try:
                termDict[term] += 1
            except(KeyError):
                termDict[term] = 1

    #TEST - check that the ten most frequent words found make sense for English
    #sort states descending by the average sentiment score of their tweets
    #freqTerms = sorted(termDict.iteritems(), key=lambda x: x[1], reverse=True)
    #for idx in xrange(0,9):
    #    print freqTerms[idx][0], freqTerms[idx][1]

    for term, frequency in termDict.iteritems():
        print term.encode('utf-8'), float(frequency) / float(Cnt)

    #gw()

if __name__ == '__main__':
    main()


