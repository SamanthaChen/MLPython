#coding=utf-8
import jieba, os
from gensim import corpora, models, similarities


train_set = []


walk = os.walk('/Reduced')
for root, dirs, files in walk:
    for name in files:
        f = open(os.path.join(root, name), 'r')
    raw = f.read()
    word_list = list(jieba.cut(raw, cut_all = False))
    train_set.append(word_list)


dic = corpora.Dictionary(train_set)
corpus = [dic.doc2bow(text) for text in train_set]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 10)
corpus_lda = lda[corpus_tfidf]

