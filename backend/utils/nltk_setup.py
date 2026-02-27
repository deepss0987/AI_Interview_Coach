import nltk
from utils.logger import logger

REQUIRED_PACKAGES = [
    "punkt",
    "stopwords",
    "wordnet",
    "omw-1.4",
    "averaged_perceptron_tagger"
]

def ensure_nltk_data():
    for pkg in REQUIRED_PACKAGES:
        try:
            nltk.data.find(pkg)
        except LookupError:
            try:
                nltk.download(pkg)
                logger.info(f"Downloaded NLTK: {pkg}")
            except Exception as e:
                logger.warning(f"Failed to download {pkg}: {e}")
