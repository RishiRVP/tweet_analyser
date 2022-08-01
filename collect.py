from getdata import TweetExtractor 

htlist = ['Ukraine', "war"]
data_collector = TweetExtractor(minlikes = 2, mincharlen = 16, tweetstofind = 300, configfilepath= 'config.json', datafolder= 'Data/', idsprocessedfile ='idsprocessedalready.txt', writeheader = True)
data_collector.InitiateAPIHAndlers()
for ht in htlist:
    print( "Collecting Tweets for hashtag #" + ht)
    print(str(data_collector.ExtractTweets('#'+ht)) + " tweets extracted for hashtag #" + ht)
    print()

    

minlikes = data_collector.rangeoflikes['min']
maxlikes = data_collector.rangeoflikes['max']
print (' Minimum Likes found are ', minlikes['val'], " for tweet id ", minlikes)
print (' Maximum Likes found are ', maxlikes['val'], " for tweet id ", maxlikes)


import json 
import os
datafolder = 'Data/JSON/'
def CheckHashTag(tweet):
    htlist = ['Service', 'price', 'Ukraine', 'war', 'economy', 'cost']
    tweettext = tweet['full_text'].lower()
    for t in htlist:
        ht = '#'+t.lower()
        if ht in tweettext:
            return True
    return False

files = os.listdir(datafolder)
files_to_check = len(files)
valid_files = 0
invalid_tweets = []
for tweetfile in files:
    jsonpath = datafolder + tweetfile
    tweetjson = json.loads(open(jsonpath,'r').read())
    if len(tweetjson['full_text'])<16 or tweetjson['favorite_count']<2 or not(CheckHashTag(tweetjson)):
        invalid_tweets.append(tweetjson)
        #print("Buggy Tweet found : ", tweetjson['full_text'].replace('\n','').strip())
    else:
        valid_files+=1
    
        
if valid_files == files_to_check:
    print ( "No invalid files found Total valid tweets collected are ", valid_files)
else:
    print(files_to_check - valid_files ," Invalid files found ")
    for t in invalid_tweets:
        pass
        print(t['id_str'],t['full_text'].replace('\n','').strip())