import tweepy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAJufYQEAAAAAKav7aNECQA0fFGEwRJ9Xre6x5uo%3Db1ceEnW5RwZTqNlXKInTamgCMDKJabKBafw6H2tUKY0qqruZby")
lemmatizer = WordNetLemmatizer()
# Class object for scrapping
class Scraper:
    def __init__(self, stock_ticker,pages ):
        self.ticker = stock_ticker
        self.data = []
        # Filling page results
        self.__scrape_pages(None, pages, self.data)
        self.__get_text()

    def __scrape_pages(self, nextToken, pages, responses):
        if pages == 0:
            return
        query = f"#{self.ticker} lang:en"
        tweets = client.search_recent_tweets(query=query,
                                         tweet_fields = ["text", "public_metrics"],
                                         max_results = 100,
                                         expansions='author_id',
                                         next_token=nextToken
                                         )
        responses.extend(tweets.data)
        # recursive call
        try:
            next_token = tweets[3]['next_token']
        except:
            return
    
        self.__scrape_pages(next_token, pages - 1, responses)
        
        
    def __get_text(self):
        text = []
        for data in self.data:
            text.append(data.text)
        self.data = text
        
        
    def __clean_text(self, data):    
        extra_stop = set(())
        stoplist = set(stopwords.words('english')) | extra_stop


        cleaned_data = data.copy()
        # Remove Mentions
        cleaned_data = [(" ".join(filter(lambda x:x[0]!='@', tweet.split()))) for tweet in cleaned_data]
        # Remove HTTPS
        cleaned_data = [(re.sub(r'http\S+', '', tweet)) for tweet in cleaned_data]
        # Remove Special Chars
        cleaned_data = [re.sub("[^a-zA-Z]+", " ", tweet) for tweet in cleaned_data]
        # Remove Stop Words

        cleaned_data = [[lemmatizer.lemmatize(word) for word in tweet.lower().split() if word not in stoplist and len(word) > 1]
                           for tweet in cleaned_data]

        cleaned_data = [" ".join(word) for word in cleaned_data]

        return cleaned_data        

    
    def get(self, no_retweets=True, clean_data=True):
        if no_retweets:
            temp_data = []
            for data in self.data:
                if "RT @" not in data:
                    temp_data.append(data)
        else:
            temp_data = self.data
            
        
        if clean_data:
            temp_data = self.__clean_text(temp_data)
        
        
        return temp_data
    
    def get_correlations(self,list_of_stocks):
        temp = []
        for i in range(len(list_of_stocks)):
            temp.append(list_of_stocks[i].lower())
        
        list_of_correlations = []
        for tweet in self.get():
            for word in tweet.split():
                if word in temp and word != self.ticker.lower():
                    list_of_correlations.append(word)
        return list_of_correlations

        