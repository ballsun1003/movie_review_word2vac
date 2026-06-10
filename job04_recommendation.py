import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec



def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]
    return recmovieList[0:11]

df_reviews = pd.read_csv('./datasets/reviews_2017_2022.csv')
Tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pkl', 'rb') as f:
    Tfidf = pickle.load(f)


ref_idx = 1228
print('title', df_reviews.iloc[ref_idx, 0])
cosine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)
print(cosine_sim[0])
print(len(cosine_sim))
recommendations = getRecommendation(cosine_sim)
print(recommendations[1:11])


#키워드 이용
embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
keyword = '이름'
if keyword not in list(embedding_model.wv.index_to_key):
    print('모르는 단어입니다.')
else:
    sim_word = embedding_model.wv.most_similar(keyword, topn=10)
    print(sim_word)
    sentence = [keyword] * 11
    count = 10
    for word, _ in sim_word:
        sentence = sentence + [word] * count
        count = count - 1
    print(sentence)
    sentence = ' '.join(sentence)
    print(sentence)

    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    recommendation = getRecommendation(cosine_sim)
    print(recommendation)