import nltk
from nltk.corpus import stopwords

# sentiment analysis  (if not found: pip install vaderSentiment at command prompt)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pattern.en import sentiment

from nltk.stem import WordNetLemmatizer

from nltk import FreqDist, word_tokenize

from os import path
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def vader_sentiment_categorized(texts):
    # initialize vader analyzer
    analyzer = SentimentIntensityAnalyzer()

    # lists of positive, negative, and neutral reviews
    positive_vader_review = []
    negative_vader_review = []
    neutral_vader_review = []

    # loop through reviews and add to appropriate list
    for sentence in texts:
        vs = analyzer.polarity_scores(sentence)
        if vs["compound"] >= 0.1:
            positive_vader_review.append(sentence)
        elif vs["compound"] <= -0.1:
            negative_vader_review.append(sentence)
        else:
            neutral_vader_review.append(sentence)
    return positive_vader_review, negative_vader_review, neutral_vader_review


def vader_overall(texts):
    analyzer = SentimentIntensityAnalyzer()
    sum = 0
    for sentence in texts:
        vs = analyzer.polarity_scores(sentence)
        sum += vs["compound"]
    return sum / len(texts)


def popular_words(documents):
    texts = [[word for word in document.lower().split()]
             for document in documents]
    texts = [x for y in texts for x in y]
    wordnet_lemmatizer = WordNetLemmatizer()
    texts = (wordnet_lemmatizer.lemmatize(word) for word in texts)
    fdist = nltk.FreqDist(texts)
    return fdist


def make_wordcloud(texts, ticker):
    texts = str(texts)
    texts = texts.replace("'", '')

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(
        max_font_size=40, relative_scaling=.5).generate(texts)
    wordcloud.to_file(f'./wordclouds/{ticker}.png')
