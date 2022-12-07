# Write your code here
# Write your code here
import string
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from lxml import etree
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# nltk.set_proxy('http://127.0.0.1:1087')
# nltk.download('averaged_perceptron_tagger')
xml_path = "news.xml"
tree = etree.parse(xml_path).getroot()
stop = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
doc_noun_list = []
doc_title_list = []
for k, v in tree[0]:
    title = k.text
    doc_title_list.append(title)

    text = v.text
    text_list_raw = word_tokenize(text.lower())
    text_list_lem = [lemmatizer.lemmatize(w) for w in text_list_raw]
    text_list = [w for w in text_list_lem if (w not in string.punctuation and w not in stop)]
    text_list.sort(reverse=True)
    pos_tag = [nltk.pos_tag([w]) for w in text_list]
    noun_list = [v[0][0] for v in pos_tag if v[0][1] == "NN"]
    noun_sent = ""
    for i in noun_list:
        noun_sent += i + " "
    doc_noun_list.append(noun_sent)

vectorizer = TfidfVectorizer(ngram_range=(1, 1))
weighted_matrix = vectorizer.fit_transform(doc_noun_list)
terms = vectorizer.get_feature_names_out()
matrix_array = weighted_matrix.toarray()

doc_word_first = []
for row in matrix_array:
    list_with_idx = [(i, v) for i, v in enumerate(row)]
    sorted_list = sorted(list_with_idx, key=lambda x: x[1], reverse=True)
    weight = 100
    list_first = []
    inner_sort = []
    for i, v in enumerate(sorted_list):
        if v[1] < weight:
            weight = v[1]
            if inner_sort:
                inner_sort.sort(reverse=True)
                for vv in inner_sort:
                    list_first.append(vv)
            # if i > 5:
            #     break
            inner_sort.clear()
        word = terms[v[0]]
        inner_sort.append(word)
    doc_word_first.append(list_first[:5])

for i, v in enumerate(doc_title_list):
    print(v + ":")
    print(*doc_word_first[i], sep=' ')
    print("")


# for k, v in tree[0]:
#     title = k.text
#     print(title + ":")
#     text = v.text
#     text_list_raw = word_tokenize(text.lower())
#     text_list_lem = [lemmatizer.lemmatize(w) for w in text_list_raw]
#     text_list = [w for w in text_list_lem if (w not in string.punctuation and w not in stop)]
#
#     text_list.sort(reverse=True)
#     pos_tag = [nltk.pos_tag([w]) for w in text_list]
#     noun_list = [v[0][0] for v in pos_tag if v[0][1] == "NN"]
#     c = Counter(noun_list)
#
#     most_freq_list = []
#     for i in c.most_common(5):
#         most_freq_list.append(i[0])
#     print(*most_freq_list, sep=' ')
#     print("")



