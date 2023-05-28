import nltk

from multi_rake import Rake
from pymystem3 import Mystem
from nltk.corpus import stopwords as stop_words


nltk.download('stopwords')
nltk.download('punkt')


class KeywordsExtractor:

    stopwords = set(stop_words.words('russian'))

    algo = Rake(
        min_chars=3,
        max_words=1,
        min_freq=1,
        language_code='ru',
        stopwords=stopwords,
        lang_detect_threshold=50,
        max_words_unknown_lang=2,
        generated_stopwords_percentile=80,
        generated_stopwords_max_len=3,
        generated_stopwords_min_freq=2,
    )

    @classmethod
    def extract_keywords(cls, from_text: str):
        tokens = nltk.word_tokenize(from_text, language='russian')
        lemmatizer = Mystem()

        lemmatized_tokens = [lemmatizer.lemmatize(token)[0] for token in tokens]
        return [pair[0] for pair in cls.algo.apply(' '.join(lemmatized_tokens)) if pair[0] not in cls.stopwords]
