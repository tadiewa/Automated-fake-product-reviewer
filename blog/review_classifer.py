import sklearn.datasets as skd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import accuracy_score
import pickle




def classify_review(review):
    categories = ['negative', 'positive']

    pl_train = skd.load_files('blog/review/train', categories=categories, encoding='ISO-8859-1')

    # pl_test=  skd.load_files('dataset/test',categories=categories,encoding='ISO-8859-1')

    print(pl_train.target_names)

    count_vect = CountVectorizer()
    X_train_tf = count_vect.fit_transform(pl_train.data)
    # X_test_tf =  count_vect.transform(pl_test.data)
    tfidf_transformer = TfidfTransformer()

    X_train_tfidf = tfidf_transformer.fit_transform(X_train_tf)
    # X_test_tfidf  = tfidf_transformer.transform(X_test_tf)
    clf = MultinomialNB().fit(X_train_tfidf, pl_train.target)


    text_to_predict =  []
    text_to_predict.append(review)
    X_new_counts = count_vect.transform(text_to_predict)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    return (clf.predict(X_new_tfidf))








