import gensim
from gensim import corpora
import TextCleaner
from Helpers import fileIO
import sklearn.feature_extraction.text
import sklearn.decomposition


data = fileIO.load_json_file('../TestData/TestProfiles.json')
clean_bios = TextCleaner.clean_text(data, 'bio')

processed_docs = clean_bios

# # create a count vectorizer object
count_vect = sklearn.feature_extraction.text.CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(processed_docs[0])

# # transform the training and validation data using count vectorizer object
# xtrain_count =  count_vect.transform(train_x)
# xvalid_count =  count_vect.transform(valid_x)

lda_model = sklearn.decomposition.LatentDirichletAllocation(n_components=20, learning_method='online', max_iter=20)
# x_topics = lda_model.fit_transform(xtrain_count)
# topic_word = lda_model.components_
vocab = count_vect.get_feature_names()
print(vocab)

# n_top_words = 10
# topic_summaries = []
#
# for i, topic_dist in enumerate(topic_word):
#     topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(n_top_words+1):-1]
#     topic_summaries.append(' '.join(topic_words))

# dictionary = corpora.Dictionary(processed_docs)
# doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_docs]
#
# lda = gensim.models.LdaModel
# lda_model = lda(doc_term_matrix, num_topics=3, id2word=dictionary, passes=50)

# print(lda_model.print_topics(num_topics=3, num_words=1))

