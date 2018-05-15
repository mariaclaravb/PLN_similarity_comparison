import os

import nltk
import numpy as np
from nltk.stem.rslp import RSLPStemmer
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import cm as cm


path = "corpus/"
token_dict = dict([])
text_list = list()
stemmer = RSLPStemmer()

stopwords = set([])
for s in open("stopwords-pt.txt", 'r').readlines():
    stopwords.add(s.strip().lower())


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text, language='portuguese'), stemmer)


def similaridade(doc_list):
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words=stopwords)
    tfidf = vectorizer.fit_transform(doc_list)
    # return 1 - ((tfidf * tfidf.T).A)[0, 1]
    return cosine_similarity(tfidf)

def plot_matrix(df):

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 15)
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap)
    ax1.grid(False)
    plt.title('DISTÂNCIA')
    labels = list_file_name
    ax1.set_xticklabels(labels, fontsize=7, rotation=30)
    ax1.set_yticklabels(labels, fontsize=7)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=np.arange(0.0, 1.0, (1/len(list_file_name))))
    plt.show()


if __name__ == '__main__':

    list_file_name = []

    for subdir, dirs, files in os.walk(path):
        list_file_name.extend([f[:-4] for f in files])
        for file in files:
            file_path = subdir + os.path.sep + file
            content = open(file_path, 'r')
            text = content.read().lower()
            token_dict[file.replace('.txt', '').title()] = text
            text_list.append(text)


    sim = similaridade(list(token_dict.values()))
    print(sim)
    # print("{}\n".format(sim))
    plot_matrix(sim)
