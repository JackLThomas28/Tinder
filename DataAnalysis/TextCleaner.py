import nltk
import sys
sys.path.append('/Users/jackthomas/Documents/School/Fall2018/cs4320 - Information Retrieval/Project/Tinder/Helpers/')
import fileIO
import string
# nltk.download('punkt')
# nltk.download('stopwords')

APOSTRAPHE = '\u2019'


def tokenize(data):
    return nltk.tokenize.word_tokenize(data)


def make_lowercase(data):
    return [word.lower() for word in data]


def remove_punctuation(data):
    table = str.maketrans('', '', string.punctuation)
    data = [word.translate(table) for word in data]
    ### Remove apostraphe not caught by string.punctuation
    data = [word for word in data if word != APOSTRAPHE]
    ### Remove any empty strings
    return [word for word in data if word != '']


def remove_stop_words(data):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    return [word for word in data if not word in stop_words]


def clean_text(data, attribute):
    text = [tokenize(data[i][attribute]) for i in range(len(data))]
    text = [make_lowercase(entry) for entry in text]
    text = [remove_punctuation(entry) for entry in text]
    text = [remove_stop_words(entry) for entry in text]
    return text


def main():
    data = fileIO.load_json_file('../TestData/TestProfiles.json')
    clean_bios = clean_text(data, 'bio')
    print(clean_bios)


main()