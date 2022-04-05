from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import tweepy
from textblob import TextBlob
# from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')


def HashtagPrediction(request):
    if request.POST:
        # Twitter Api Credentials
        consumerKey = 'hC02vDfkSX1IBYOZPRjCpgXCm'
        consumerSecret = 'Pm080QkpceLW3Q1RKBRIIZDI3Nn1khMogxUeB2KyJjFqIamr6i'
        accessToken = '1321309664772907008-NT3w9KrGuT4BzsCKHdiFEgq8HamZ9B'
        accessTokenSecret = 'fkudHFKdUlbkaGLUwnNGeEU2MxpPVKC1nqkEGpVmAqk3S'
    
        
        # Create the authentication object
        authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
            
        # Set the access token and access token secret
        authenticate.set_access_token(accessToken, accessTokenSecret) 
            
        # Creating the API object while passing in auth information
        api = tweepy.API(authenticate, wait_on_rate_limit = True)
        
        # Extract 100 tweets from the twitter user
        user_name = request.POST['name']
        # counts = request.POST['count']
        # posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")
        # posts = api.user_timeline(screen_name="BillGates", count = 100, lang ="en", tweet_mode="extended")


        search_words = str(user_name)

        # tweets = tweepy.Cursor(api.search, q=search_words, lang="en").items(1000)
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en").items(5)

        posts = []
        for i in tweets:
        #     print(i)
            posts.append(i)

        print(posts)
        
        #  Print the last 5 tweets
        print("Show the 5 recent tweets:\n")
        i=1
        for tweet in posts[:2]:
            print(str(i) +') '+ tweet.text + '\n')
            i= i+1
            print(i)
        
        # Create a dataframe with a column called Tweets
        df = pd.DataFrame([tweet.text for tweet in posts], columns=['Tweets'])
        # Show the first 5 rows of data
        # data = str(df.head())
        
        # Create a function to clean the tweets
        def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('RT[\s]+', '', text) # Removing RT
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text


        # Clean the tweets
        df['Tweets'] = df['Tweets'].apply(cleanTxt)

        # Show the cleaned tweets
        # data = str(df)
        
        # Create a function to get the subjectivity
        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

        # Create a function to get the polarity
        def getPolarity(text):
            return  TextBlob(text).sentiment.polarity


        # Create two new columns 'Subjectivity' & 'Polarity'
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)

        # Show the new dataframe with columns 'Subjectivity' & 'Polarity'
        # data = str(df)
        
        # word cloud visualization
        # allWords = ' '.join([twts for twts in df['Tweets']])
        # wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)


        # plt.imshow(wordCloud, interpolation="bilinear")
        # plt.axis('off')
        # plt.show()
        
        # Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
        def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        # Show the dataframe
        # data = str(df)
        
        # Printing positive tweets 
        # print('Printing positive tweets:\n')
        # j=1
        # sortedDF = df.sort_values(by=['Polarity']) #Sort the tweets
        # for i in range(0, sortedDF.shape[0] ):
        #     if(sortedDF['Analysis'][i] == 'Positive'):
        #         print(str(j) + ') '+ sortedDF['Tweets'][i])
        #         print()
        #         j= j+1
        #         print(j)
        
        
        # Printing negative tweets  
        # print('Printing negative tweets:\n')
        # j=1
        # sortedDF = df.sort_values(by=['Polarity'],ascending=False) #Sort the tweets
        # for i in range(0, sortedDF.shape[0] ):
        #     if( sortedDF['Analysis'][i] == 'Negative'):
        #         print(str(j) + ') '+sortedDF['Tweets'][i])
        #         print()
        #         j=j+1
        
        # Plotting 
        # plt.figure(figsize=(8,6)) 
        # for i in range(0, df.shape[0]):
        #     plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue') 
        # # plt.scatter(x,y,color)   
        # plt.title('Sentiment Analysis') 
        # plt.xlabel('Polarity') 
        # plt.ylabel('Subjectivity') 
        # plt.show()
        data = ""
        pos = 0.0
        neg = 0.0
        net = 0.0
        # Print the percentage of positive tweets
        ptweets = df[df.Analysis == 'Positive']
        ptweets = ptweets['Tweets']
        # ptweets

        try:
            pos = float(round((ptweets.shape[0] / df.shape[0]) * 5, 1))
        
            # Print the percentage of negative tweets
            ntweets = df[df.Analysis == 'Negative']
            ntweets = ntweets['Tweets']
            ntweets
        except:
            messages.add_message(request, messages.ERROR, 'Enter Proper Hash Tag ...')
            return render(request,'HashtagPrediction.html')

        neg = float(round((ntweets.shape[0] / df.shape[0]) * 5, 1))
        
        net = float(100 - (pos+neg))
        
        # Show the value counts
        data = df['Analysis'].value_counts()
        pos = float(data[0])
        print(pos,"This is pos")
        neg = float(data[2])
        print(neg,"This is neg")
        net = float(data[1])
        print(net,"This is net")
        
        
        # Plotting and visualizing the counts
        plt.title(f"{user_name}'s Response Analysis")
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df['Analysis'].value_counts().plot(kind = 'bar')
        path = settings.BASE_DIR+"/app1/static/media/OutPut.png"
        plt.savefig(path)
        
        data = 'media/OutPut.png'
        
        return render(request,'HashtagPrediction.html',{'data':path,'pos':pos,'neg':neg,'net':net})
    return render(request,'HashtagPrediction.html')




def Polarity(request):
    if request.POST:
        file1 = str(settings.BASE_DIR+"/app1/static/media/ftable.csv")
        ftable = pd.read_csv(file1)
        ftable = ftable[ftable['word'] != 'sad']
        ftable = ftable[ftable['word'] != 'sad,']
        ftable = ftable[ftable['word'] != ':(']
        ftable = ftable[ftable['word'] != 'fun']
        ftable = ftable[ftable['word'] != 'happy,']
        ftable = ftable[ftable['word'] != 'happy']
        ftable = ftable.drop_duplicates(subset = 'word')

        test = str(request.POST['text'])
        # test = input("Enter Tweet = ")
        # test = '@LindaLindae9 Such a sad, sad thing...there was NO reason for those young deaths.😪'
        positive_instance = 24070.0
        negative_instance = 23930.0

        #split all the words in my text
        test_words = test.split()

        prob_positive = float(positive_instance/(positive_instance+negative_instance))
        prob_negative = 1 - prob_positive

        pos_word = 1.0*prob_positive
        neg_word = 1.0*prob_negative
        for i in range(len(test_words)):
            word = test_words[i]
            # print(word)
            index_val = ftable.index[ftable['word'] == word]
            if (len(index_val) > 0):
                print(index_val[0])
                pos_val = ftable['positive'].iloc[index_val[0]]
                neg_val = ftable['negative'].iloc[index_val[0]]
                pos_word = pos_word * pos_val/positive_instance
                neg_word = neg_word * neg_val/negative_instance
        
        data = ""
        val = 0
        if pos_word > neg_word:
            data += "The sentence was POSITIVE, with a probability of"
            val = pos_word/(pos_word+neg_word)
        else:
            data += "The sentence was NEGATIVE, with a probability of"
            val = neg_word/(pos_word+neg_word)
        return render(request,'polarity.html',{'data':data,'val':val})
    return render(request,'polarity.html')


