from .markov import *

def write_sonnet():
    new_sonnet = []

    for i in range(0, 14):
        file = 'app/static/sonnets.txt'
        string_list = open(file).read().split('\n')
        source_tweets = []

        for item in string_list:
            # Tests to get rid of empty lines, roman numeral lines
            if item != '' and not item.startswith("XC") and not item.startswith("LX") and not item.startswith("II") and not item.startswith("IV") and not item.startswith("VI") and not item.startswith("CX") and not item.startswith("L.") and not item.startswith("C.") and not item.startswith("CL") and not item.startswith("LI.") and not item.startswith("LII"):
                source_tweets.append(item)

        mine = MarkovChainer(3)
        for tweet in source_tweets:
            if re.search('([\.\!\?\"\']$)', tweet):
                pass
            else:
                tweet+="."
            mine.add_text(tweet)

        for x in range(0,10):
            ebook_tweet = mine.generate_sentence()
            ebook_tweet += " " + mine.generate_sentence().lower()
            ebook_tweet += " " + mine.generate_sentence().lower()

        #if a tweet is very short, this will randomly add a second sentence to it.
        if ebook_tweet != None and len(ebook_tweet) < 40:
            newer_tweet = mine.generate_sentence()
            if newer_tweet != None:
                ebook_tweet += " " + mine.generate_sentence()
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

            new_sonnet.append(ebook_tweet)

        elif ebook_tweet == None:
            print("Tweet is empty, sorry.")
        else:
            print("TOO LONG: " + ebook_tweet)

    return new_sonnet
