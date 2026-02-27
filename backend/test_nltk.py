from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = 'hello , this is deepali gupta , nice to meet you!'

tokens = word_tokenize(text)
clean_tokens = [t for t in tokens if t not in stopwords.words('english')]

print('tokens :' ,tokens)
print("clean tokens :" , clean_tokens)