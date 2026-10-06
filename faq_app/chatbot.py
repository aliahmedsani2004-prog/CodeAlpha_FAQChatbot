
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .faqs import FAQS

# NLTK ka data project ke andar nltk_data folder mein hai
nltk.data.path.append(str(Path(__file__).resolve().parent.parent / "nltk_data"))

tokenizer = RegexpTokenizer(r"[a-z0-9]+")
stemmer = PorterStemmer()
STOP_WORDS = set(stopwords.words("english"))

THRESHOLD = 0.25  # isse kam match ho toh bot "samajh nahi aaya" bolega
FALLBACK = "Sorry, I couldn't find an answer to that. Please contact support@shopeasy.com."


def preprocess(text):
    """Text saaf karo: lowercase, tokenize, stopwords hatao, stemming."""
    tokens = tokenizer.tokenize(text.lower())
    return " ".join(stemmer.stem(t) for t in tokens if t not in STOP_WORDS)


# Server start hote hi ek baar FAQ questions ko vectors mein badal lo
_questions = [preprocess(f["question"]) for f in FAQS]
_vectorizer = TfidfVectorizer()
_faq_vectors = _vectorizer.fit_transform(_questions)


def get_answer(user_question):
    """User ke sawaal ka sabse milta-julta FAQ dhundo. (answer, score) wapas karta hai."""
    cleaned = preprocess(user_question)
    if not cleaned:
        return FALLBACK, 0.0

    user_vector = _vectorizer.transform([cleaned])
    scores = cosine_similarity(user_vector, _faq_vectors)[0]

    best_index = scores.argmax()
    best_score = float(scores[best_index])

    if best_score < THRESHOLD:
        return FALLBACK, best_score
    return FAQS[best_index]["answer"], best_score