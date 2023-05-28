from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()


class SentimentAnalyzer:
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    @classmethod
    def analyze_sentiment(cls, from_text) -> float:
        """Returns value from -1 to 1 where -1 is the most negative, 0 is neutral, 1 is the most positive"""

        sentiment = cls.model.predict([from_text], k=2)[0]

        if max(sentiment.get('skip', 0), sentiment.get('neutral', 0)) >= max(sentiment.get('positive', 0), sentiment.get('negative', 0)):
            return 0  # if hesitating count as neutral
        if sentiment.get('positive', 0) > sentiment.get('negative', 0):
            return sentiment.get('positive', 0)
        return -sentiment.get('negative', 0)



