# Install Libraries
# 1.pip install textblob
# 2.pip install tweepy
# 3. anyother relevent librarires for the below mentioned import

# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from cv2 import *
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, appcontext_popped, appcontext_tearing_down, request, render_template

# Authentication
def authenti():
	app = Flask(__name__)
    
@appcontext_popped.route('/')
def my_form():
    return render_template('pg.html')
@appcontext_popped.route('/', methods=['POST'])

consumerKey = request.form['consumerKey']
consumerSecret = request.form['consumerSecret']
accessToken = request.form['accessToken']
accessTokenSecret = request.form['accessTokenSecret']
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Sentiment Analysis
def percentage(part,whole):
 return 100 * float(part)/float(whole)

keyword = input(request.form['hashtaga'] )
noOfTweet = int(input (request.form['no_of_tweets'] ))
tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
for tweet in tweets:
 
 #print(tweet.text)
 tweet_list.append(tweet.text)
 analysis = TextBlob(tweet.text)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
 neg = score["neg"]
 neu = score["neu"]
 pos = score["pos"]
 comp = score["compound"]
 polarity += analysis.sentiment.polarity
 
if neg > pos:
 negative_list.append(tweet.text)
 negative += 1
elif pos > neg:
 positive_list.append(tweet.text)
 positive += 1
 
elif pos == neg:
 neutral_list.append(tweet.text)
 neutral += 1
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, ".1f")
negative = format(negative, ".1f")
neutral = format(neutral, ".1f")


#Number of Tweets (Total, Positive, Negative, Neutral)
def discribe():
	tweet_list = pd.DataFrame(tweet_list)
	neutral_list = pd.DataFrame(neutral_list)
	negative_list = pd.DataFrame(negative_list)
	positive_list = pd.DataFrame(positive_list)
	print("total number: ",len(tweet_list))
	print("positive number: ",len(positive_list))
	print("negative number: ", len(negative_list))
	print("neutral number: ",len(neutral_list))

#Creating PieCart
def pie(): 
	labels = ["Positive ["+str(positive)+"%]" , "Neutral ["+str(neutral)+"%]","Negative ["+str(negative)+"%]"]
	sizes = [positive, neutral, negative]
	colors = ["yellowgreen", "blue","red"]
	patches, texts = plt.pie(sizes,colors=colors, startangle=90)
	plt.style.use("default")
	plt.legend(labels)
	plt.title("Sentiment Analysis Result for keyword= "+keyword+"" )
	plt.axis("equal")
	plt.show()

#Function to Create Wordcloud
def create_wordcloud(text):
 	mask = np.array(Image.open("cloud.png"))
 	stopwords = set(STOPWORDS)
 	wc = WordCloud(background_color="white",mask = mask,max_words=3000,stopwords=stopwords,repeat=True)
 	wc.generate(str(text))
 	wc.to_file("wc.png")
 	print("Word Cloud Saved Successfully")
 	path="wc.png"
 	display(Image.open(path))
#Creating wordcloud for all tweets
create_wordcloud(tw_list["text"].values)