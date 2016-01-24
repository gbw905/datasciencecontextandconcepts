import sys
import json
import re

def hw():
    print 'Start Run ' + sys.argv[0]

def gw():
    print 'End Run ' + sys.argv[0]

def getState(text):
    stateAbrev = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NA', 'NC', 'ND','NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY' ]
    stateNames = ['Alaska','Alabama','Arkansas','American Samoa','Arizona','California','Colorado','Connecticut','District of Columbia','Delaware','Florida','Georgia','Guam','Hawaii','Iowa','Idaho','Illinois','Indiana','Kansas','Kentucky','Louisiana','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri','Northern Mariana Islands','Mississippi','Montana','National','North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico','Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Virgin Islands','Vermont','Washington','Wisconsin','West Virginia','Wyoming']
    stateDict = {'Alaska':'AK', 'Alabama':'AL', 'Arkansas':'AR', 'American Samoa':'AS', 'Arizona':'AZ', 'California':'CA', 'Colorado':'CO', 'Connecticut':'CT', 'District of Columbia':'DC', 'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Guam':'GU', 'Hawaii':'HI', 'Iowa':'IA', 'Idaho':'ID', 'Illinois':'IL', 'Indiana':'IN', 'Kansas':'KS', 'Kentucky':'KY', 'Louisiana':'LA', 'Massachusetts':'MA', 'Maryland':'MD', 'Maine':'ME', 'Michigan':'MI', 'Minnesota':'MN', 'Missouri':'MO', 'Northern Mariana Islands':'MP', 'Mississippi':'MS', 'Montana':'MT', 'National':'NA', 'North Carolina':'NC', 'North Dakota':'ND', 'Nebraska':'NE', 'New Hampshire':'NH', 'New Jersey':'NJ', 'New Mexico':'NM', 'Nevada':'NV', 'New York':'NY', 'Ohio':'OH', 'Oklahoma':'OK', 'Oregon':'OR', 'Pennsylvania':'PA', 'Puerto Rico':'PR', 'Rhode Island':'RI', 'South Carolina':'SC', 'South Dakota':'SD', 'Tennessee':'TN', 'Texas':'TX', 'Utah':'UT', 'Virginia':'VA', 'Virgin Islands':'VI', 'Vermont':'VT', 'Washington':'WA', 'Wisconsin':'WI', 'West Virginia':'WV', 'Wyoming':'WY'}
    try:
        words = text.split()
        for word in words:
            if word.strip() in stateAbrev:
                return word.strip()
            if word.strip() in stateNames:
                return stateDict[word.strip()]
    except:
        return "here"
    return "here"

def main():
    #hw()
    score_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #load sentiment scoring dictionary from 'score_file'
    scores = {} # initialize an empty dictionary
    for line in score_file:
        term, score = line.split("\t") # The file is tab delimited
        scores[term] = int(score) # convert the score to an integer

    #extract tweets and user location
    tweets = []
    for line in tweet_file:
        d = json.loads(line)
        if "text" in d.keys():
            tweets.append([d["text"],getState(d["user"]["location"])])

    #sum the total sentiment for the state AND count the number of tweets per state    
    locationDict = {}
    locationCnt = {}
    for tweet in tweets:
        total = 0
        encoded_tweet = tweet[0].encode('utf-8')
        words = encoded_tweet.split()
        for word in words: #remove words that cannot be a sentiment
            if word.startswith("RT") or word.startswith("www") or word.startswith("http"):
                words.remove(word)
        unwanted = re.compile('[^A-Za-z]+') #remove characters not used in our sentiment dictionary
        words = [unwanted.sub("", word) for word in words]
        if len(words) > 0:
            for word in words:
                if word.strip() in scores: 
                    total = total + scores[word.strip()]
            try:
                locationDict[tweet[1]] += total
                locationCnt[tweet[1]] += 1
            except(KeyError):
                locationDict[tweet[1]] = total
                locationCnt[tweet[1]] = 1
    
    #calculate the average sentiment score for each state
    hLocs = {}
    for hLoc in locationDict.iteritems():
        hLocs[hLoc[0]] = float(hLoc[1])/float(locationCnt[hLoc[0]])

    #sort states descending by the average sentiment score of their tweets
    happyLocations = sorted(hLocs.iteritems(), key=lambda x: x[1], reverse=True)

    #print the top ten states
    #for idx in xrange(0,9):
    #    print happyLocations[idx][0], happyLocations[idx][1]
    print happyLocations[0][0]

    #gw()

if __name__ == '__main__':
    main()


