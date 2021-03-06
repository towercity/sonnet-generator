import random
import re
import sys
import markov

def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        numero = n2c[guess]
        try:
            text = unichr(numero)
        except KeyError:
            pass
    return text

def filter_tweet(tweet):
    tweet.text = re.sub(r'\b(RT|MT) .+','',tweet.text) #take out anything after RT or MT
    tweet.text = re.sub(r'(\#|@|(h\/t)|(http))\S+','',tweet.text) #Take out URLs, hashtags, hts, etc.
    tweet.text = re.sub(r'\n','', tweet.text) #take out new lines.
    tweet.text = re.sub(r'\"|\(|\)', '', tweet.text) #take out quotes.
    htmlsents = re.findall(r'&\w+;', tweet.text)
    if len(htmlsents) > 0 :
        for item in htmlsents:
            tweet.text = re.sub(item, entity(item), tweet.text)
    tweet.text = re.sub(r'\xe9', 'e', tweet.text) #take out accented e
    return tweet.text



def grab_tweets(api, max_id=None):
    source_tweets = []
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    max_id = user_tweets[len(user_tweets)-1].id-1
    for tweet in user_tweets:
        tweet.text = filter_tweet(tweet)
        if len(tweet.text) != 0:
            source_tweets.append(tweet.text)
    return source_tweets, max_id

if __name__=="__main__":
    order = 3
    sonnet_number = random.randrange(155, 647)
    sonnet_lines = []

    print("")
    print("Sonnet number", sonnet_number)
    print("")

    for i in range(0, 12):
        file = 'sonnets.txt'
        string_list = open(file).read().split('\n')
        source_tweets = []

        for item in string_list:
            # Tests to get rid of empty lines, roman numeral lines
            if item != '' and not item.startswith("XC") and not item.startswith("LX") and not item.startswith("II") and not item.startswith("IV") and not item.startswith("VI") and not item.startswith("CX") and not item.startswith("L.") and not item.startswith("C.") and not item.startswith("CL") and not item.startswith("LI.") and not item.startswith("LII"):
                source_tweets.append(item)

        mine = markov.MarkovChainer(order)
        for tweet in source_tweets:
            if re.search('([\.\!\?\"\']$)', tweet):
                tweet+=" "
            else:
                tweet+="."
            mine.add_text(tweet)

        for x in range(0,10):
            ebook_tweet = mine.generate_sentence()
            ebook_tweet += " %s" % (mine.generate_sentence().lower())
            ebook_tweet += " %s" % (mine.generate_sentence().lower())

        #if a tweet is very short, this will randomly add a second sentence to it.
        if ebook_tweet != None and len(ebook_tweet) < 40:
            newer_tweet = mine.generate_sentence()
            if newer_tweet != None:
                ebook_tweet += " %s" % (mine.generate_sentence().lower())
            else:
                ebook_tweet = ebook_tweet

        #throw out tweets that match anything from the source account.
        if ebook_tweet != None and len(ebook_tweet) < 110:
            for tweet in source_tweets:
                if ebook_tweet[:-1] not in tweet:
                    continue
                else:
                    print ("TOO SIMILAR: " + ebook_tweet)
                    sys.exit()


            sonnet_lines.append(ebook_tweet)

        elif ebook_tweet == None:
            print("Tweet is empty, sorry.")
        else:
            print("TOO LONG: " + ebook_tweet)

    for line in sonnet_lines:
        print(line)
