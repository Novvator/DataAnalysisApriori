# Import libraries
import tarfile
import string
import nltk
import os
import pickle
import numpy as np
import urllib.request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Download nltk words data
nltk.download('stopwords')

if os.path.isfile("preprocessed_data_stemmer_1.pkl"):
    # Load previously generated data
    with open("preprocessed_data_stemmer_1.pkl", "rb") as f:
        preprocessed_text_data = pickle.load(f)
        list_data = pickle.load(f)
else:
    filename = "20news-bydate.tar.gz"

    # Download file
    if not os.path.isfile(filename):
        url = 'http://qwone.com/~jason/20Newsgroups/' + filename
        urllib.request.urlretrieve(url, filename)
    
    # Unzip the file
    tar = tarfile.open(filename, "r:gz")
    tar.extractall()
    tar.close()

    # Load the data
    data = []
    path = "20news-bydate-train"
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file), "r", encoding='utf-8', errors='ignore') as f:
                text = f.read()
                lines = text.strip().split("\n")
                start = 0
                for i, line in enumerate(lines):
                    if line.startswith("Lines:"):
                        start = i + 1
                        text = "\n".join(lines[start:])
                        break
                data.append(text)
                

    # Preprocess the data
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    punctuation_map = str.maketrans("", "", string.punctuation)
    preprocessed_text_data = []
    for text in data:
        text = text.translate(punctuation_map)
        words = nltk.word_tokenize(text)
        words = [word.lower() for word in words if word.isalpha()]
        words = [stemmer.stem(word) for word in words if word not in stop_words]
        words = [word for word in words if word not in stop_words]
        preprocessed_text_data.append(" ".join(words))

    # Convert data to appropriate form for apriori
    list_data = [[item] for item in preprocessed_text_data]
    list_data = [sublist[0].split() for sublist in list_data]

    # Store the preprocessed data
    with open("preprocessed_data_stemmer_1.pkl", "wb") as f:
        pickle.dump(preprocessed_text_data, f)
        pickle.dump(list_data, f)

# Calculate tf-idf
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_text_data)

# # Find the top-k words based on tf-idf
k = 10
feature_names = vectorizer.get_feature_names_out()
tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
top_k = [feature_names[i] for i in tfidf_sorting[:k]]
print("Top-{} words based on tf-idf: {}".format(k, top_k))

# Encode data to transactions and then to pandas dataframe for apriori
transaction_encoder = TransactionEncoder()
encoded_transactions = transaction_encoder.fit(list_data).transform(list_data)
df = pd.DataFrame(encoded_transactions, columns=transaction_encoder.columns_)

# Find frequent item sets with min support
frequent_itemsets = apriori(df, min_support=0.15, use_colnames=True)

# Find association rules with min confidence
association_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)
print(association_rules)
