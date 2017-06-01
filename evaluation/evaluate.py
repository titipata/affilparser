"""Evaluate all models
"""

import affilparser
import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
import sklearn_crfsuite
from sklearn_crfsuite import metrics

NLP = spacy.load('en')

def row2tokens(row):
    tokens = []
    for token in NLP(row['raw_text']):
        if token.text in row['department']:
            tokens.append((token.text, token.pos_, 'department'))
        elif token.text in row['institution']:
            tokens.append((token.text, token.pos_, 'institution'))
        elif token.text in row['address']:
            tokens.append((token.text, token.pos_, 'address'))
        elif token.text in row['city']:
            tokens.append((token.text, token.pos_, 'city'))
        elif token.text in row['state']:
            tokens.append((token.text, token.pos_, 'state'))
        elif token.text in row['country']:
            tokens.append((token.text, token.pos_, 'country'))
        elif token.text in row['postal_box']:
            tokens.append((token.text, token.pos_, 'postal_box'))
        elif token.text == row['postal_code']:
            tokens.append((token.text, token.pos_, 'postal_code'))
        else:
            tokens.append((token.text, token.pos_, 'unknown'))
    return tokens

def sent2labels(sent):
    return [label for token, postag, label in sent]

def create_dataset():
    grobid_df = pd.read_csv('evaluation/affiliations_grobid.csv').fillna('')
    grobid_training = []
    for _, row in grobid_df.iterrows():
        row = dict(row)
        grobid_training.append(row2tokens(row))
    return grobid_training

def generate_features(grobid_training):
    ap = affilparser.AffiliationParser()
    X = [ap.token2features(gt) for gt in grobid_training]
    y = [sent2labels(gt) for gt in grobid_training]
    return X, y

def evaluate_crf(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
    )
    crf.fit(X_train, y_train)

    labels = list(crf.classes_)
    labels.remove('unknown')
    y_pred = crf.predict(X_test)
    metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=labels)

    sorted_labels = sorted(
    labels,
    key=lambda name: (name[1:], name[0])
)
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=sorted_labels, digits=3
    ))

    from collections import Counter

    def print_transitions(trans_features):
        for (label_from, label_to), weight in trans_features:
            print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))

    print("Top likely transitions:")
    print_transitions(Counter(crf.transition_features_).most_common(20))

    print("\nTop unlikely transitions:")
    print_transitions(Counter(crf.transition_features_).most_common()[-20:])


if __name__ == "__main__":
    print("loading training data and generating features")
    X, y = generate_features(create_dataset())
    print("evaluating CRF model")
    evaluate_crf(X, y)
