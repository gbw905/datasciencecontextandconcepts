import sys
import json
import re

def hw():
    print 'Start Run ' + sys.argv[0]

def gw():
    print 'End Run ' + sys.argv[0]

def lines(fp):
    print str(len(fp.readlines()))

def getKey(item):
    return item[0]

def main():
    #hw()
    score_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #load the sentiment scoring dictionary
    scores = {} # initialize an empty dictionary
    for line in score_file:
        term, score = line.split("\t") # The file is tab delimited
        scores[term] = int(score) # convert the score to an integer

    #extract the English language text from tweets
    #confession: If I include languages other than english, I will not know if 
    #logic is reasonable as I know english well. No offense to speakers of other languages
    tweets = []
    for line in tweet_file:
        d = json.loads(line)
        #if "text" in d.keys() and "lang" in d.keys():
        #    if d["lang"] == "en":
        if "text" in d.keys():
            tweets.append(d["text"])

    #calculate the average sentiment for each tweet. 
    #record the average sentiment for the tweet as the sentiment for words not yet scored
    #count the number of times each unscored word occurs
    scoreless = {}
    scorelessCnt = 0
    for tweet in tweets:
        total = 0
        tempScoreless = []
        encoded_tweet = tweet.encode('utf-8')
        words = encoded_tweet.split()
        #for word in words: #remove words that cannot be a sentiment
        #    if word.startswith("RT") or word.startswith("www") or word.startswith("http"):
        #        words.remove(word)
        unwanted = re.compile('[^A-Za-z]+') #remove characters not used in our sentiment dictionary
        words = [unwanted.sub("", word) for word in words]
        if len(words) > 0:
            for word in words:
                if word.strip() in scores: #accumulate the score for words in our sentiment dictionary
                    total = total + scores[word.strip()]
                else: #track the unscored words
                    if word.strip() is not "": tempScoreless.append(word.strip())
            #assign each unscored word the average score of the co-occuring words
            for tempW in tempScoreless: #assign unscored words the average score of scored words
                scoreless[tempW] = 0
                if len(words) - len(tempScoreless) > 0:
                    scoreless[tempW] = total / (len(words) - len(tempScoreless))

    for scored, frequency in sorted(scoreless.iteritems()):
        print scored.encode('utf-8'), float(frequency)

    return

    #sort the unscored words by word
    newScores = sorted(scoreless)

    #agregate scores for each unscored word
    #divide by the total number of occurences each unscored word
    #to get its average sentiment score
    newScoresDict = {}
    lastKey = " "
    for newScore in newScores: #caculate the average score for each unscored word
        if newScore[0] != lastKey:
            if lastKey != " ": 
                newScoresDict[lastKey] = float(total)/float(freq)
            lastKey = getKey(newScore)
            total = 0
            freq = 0
        total = total + newScore[1]
        freq = freq + 1 #accumulate the frequency with which the word occurs in all tweets sampled
    if lastKey != "": #add the last word processed to the dictionary
        newScoresDict[lastKey] = total/freq

    #Note: use of sorted list performed less well than using a dictionary to update the value for
    #      each key. In the rest of the assignment, i have not used the sort

    #for scored, frequency in sorted(newScoresDict.iteritems()):
    #    print scored.encode('utf-8'), float(frequency)

    #gw()

if __name__ == '__main__':
    main()


