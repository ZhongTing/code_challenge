import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import cross_val_score
from sklearn.svm import LinearSVC


def load_data_from_file(file_name):
    data = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            line_split = line.split()
            try:
                score = int(line_split[0])
                if abs(score) > 2:
                    score = 2 * 1 if score > 0 else -1
                data.append({"score": score, "sentence": " ".join(line_split[1:])})
            except ValueError:
                # score information missing
                pass
    return data


def vectorize(data_set):
    corpus = []
    for data in data_set:
        token_list = jieba.cut(data["sentence"])
        data["tokenize_sentence"] = " ".join(token_list)
        corpus.append(data["tokenize_sentence"])
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(corpus)
    for data in data_set:
        data["vector"] = vectorizer.transform([data["tokenize_sentence"]]).toarray()[0]


def load():
    vectors = []
    scores = []
    data_set = load_data_from_file("Ch_trainfile_Sentiment_3000.txt")
    vectorize(data_set)
    for data in data_set:
        vectors.append(data["vector"])
        scores.append(data["score"])
    return vectors, scores


def main():
    X, Y = load()
    clfs = [LinearSVC(), LogisticRegressionCV()]
    for clf in clfs:
        scores = cross_val_score(clf, X, Y, cv=5)
        score = scores.mean()
        print(score, clf)


if __name__ == "__main__":
    main()
