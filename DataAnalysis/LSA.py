from gensim import corpora
import TextCleaner
from Helpers import fileIO
from sklearn.feature_extraction.text import TfidfVectorizer


# test_data = fileIO.load_json_file('../TestData/TestProfiles.json')
train_data = fileIO.load_json_file('../TrainingData/TrainingProfiles.json')
data = fileIO.load_json_file('../DataCollection/GirlsTinderProfiles.json')

# clean_test_docs = TextCleaner.clean_text(test_data, 'bio')
clean_train_docs = TextCleaner.clean_text(train_data, 'bio')
clean_docs = TextCleaner.clean_text(data, 'bio')

print('Total Profiles Collected %d:' %len(clean_docs))

num_of_topics = 13
words = 5

dictionary = corpora.Dictionary(clean_docs)

docs = []
for doc in clean_docs:
    bio = ''
    for word in doc:
        bio += word + ' '
    if doc:
        docs.append(bio)
print('Non-empty Profiles: %d' % len(docs))

vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1, 2))
X = vectorizer.fit_transform(docs)
terms = vectorizer.get_feature_names()
print(terms)

from sklearn.decomposition import TruncatedSVD
lsa = TruncatedSVD(algorithm='randomized', n_components=5, n_iter=10)
features = lsa.fit_transform(X)

for i, comp in enumerate(lsa.components_):
    terms_in_comp = zip(terms, comp)
    sorted_terms = sorted(terms_in_comp, key=lambda x: x[1], reverse=True)[:8]
    print('Concept %d:' % i)
    for term in sorted_terms:
        print(term[0])
    print(' ')
