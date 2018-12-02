import TextCleaner
from Helpers import fileIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def get_tfifd_vectorizer(n_gram):
    return TfidfVectorizer(use_idf=True, ngram_range=n_gram)


def get_tfidf_matrix(vectorizer, documents):
    return vectorizer.fit_transform(documents)


def get_feature_names(vectorizer):
    return vectorizer.get_feature_names()


def get_lsa_model(num_topics):
    return TruncatedSVD(algorithm='randomized', n_components=num_topics, n_iter=10)


def get_features(lsa, feature_matrix):
    return lsa.fit_transform(feature_matrix)




def main():
    # Load the documents
    data = fileIO.load_json_file('../DataCollection/GirlsTinderProfiles.json')

    # Pre-process the documents
    clean_docs = TextCleaner.clean_text(data, 'bio')

    print('Total Profiles Collected %d:' % len(clean_docs))

    # Turn the list of lists into just a list of the documents
    docs = []
    for doc in clean_docs:
        bio = ''
        for word in doc:
            bio += word + ' '
        if doc:
            bio = bio[:-1]
            docs.append(bio)

    print('Non-empty Profiles: %d' % len(docs))

    # Defines
    CONCEPT_COUNT = 5
    TERM_COUNT = 8
    N_GRAM = (1, 2)

    vectorizer = get_tfifd_vectorizer(N_GRAM)
    feature_matrix = get_tfidf_matrix(vectorizer, docs)
    features = get_feature_names(vectorizer)

    lsa = get_lsa_model(CONCEPT_COUNT)
    get_features(lsa, feature_matrix)

    for i, component in enumerate(lsa.components_):
        terms_in_comp = zip(features, component)
        sorted_terms = sorted(terms_in_comp, key=lambda x: x[1], reverse=True)[:TERM_COUNT]
        print('Concept %d:' % i)
        for term in sorted_terms:
            print(term[0])
            print(term)
        print(' ')


if __name__ == '__main__':
    main()
