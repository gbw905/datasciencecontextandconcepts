import sys
import json
import re, string

def hw(): #hello world
    print 'Start Run ' + sys.argv[0]

def gw(): #goodbye world
    print 'End Run ' + sys.argv[0]

def lines(fp):
    print str(len(fp.readlines()))

def getKey(item):
    return item[0]

def main():
    #hw()
    score_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #load the dictionary for scoring word sentiment
    scores = {} # initialize an empty dictionary
    for line in score_file:
        term, score = line.split("\t") # The file is tab delimited
        scores[term] = int(score) # convert the score to an integer

    #read the english language text for each tweet into a table
    #Note: this is my limitation. Since english is the only language I
    #      understand well, I wouldn't know if the results made sense
    #      if I included other languages
    tweets = []
    for line in tweet_file:
        d = json.loads(line)
        #if "text" in d.keys() and "lang" in d.keys():
        #    if d["lang"] == "en":
        if "text" in d.keys():
            tweets.append(d["text"])

    #score tweets for sentiment and print the scores
    for tweet in tweets:
        total = 0
        encoded_tweet = tweet.encode('utf-8')
        words = encoded_tweet.split()
        for word in words: #remove words that cannot be a sentiment
            if word.startswith("RT") or word.startswith("www") or word.startswith("http"):
                words.remove(word)
        unwanted = re.compile('[^A-Za-z_]+') #remove characters not used in our sentiment dictionary
        words = [unwanted.sub("", word) for word in words]
        if len(words) > 0:
            for word in words:
                if word.strip() in scores: #accumulate the score for words in our sentiment dictionary
                    total = total + scores[word.strip()]
            print float(total)

    #gw()

if __name__ == '__main__':
    main()


