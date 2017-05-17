import spacy
import pycrfsuite
import numpy as np
import pandas as pd
from affiliation_parser import parse_affil

nlp = spacy.load('en')

def get_unique_affiliation(affiliation_list):
    """
    Get unique affilaitions for given affiliation string
    from MEDLINE
    """
    affiliations, affiliations_split = [], []
    for affil in affiliation_list:
        if '\n' in affil:
            affiliations.extend([a_ for a_ in affil.split('\n')])
        elif ';' in a:
            affiliations.extend([a_ for a_ in affil.split(';')])
        else:
            affiliations.append(affil)
    affiliations = pd.unique(affiliations)
    for affil in affiliations:
        affiliations_split.extend(affil.split('; '))
    affiliations_split = pd.unique(affiliations_split)
    return affiliations_split

def affil2token(affiliation_text):
    """
    Using rule-based parse affiliation to parse affiliation

    Input
    =====
    affiliation_text: str, affiliation string from MEDLINE

    Output
    ======
    token_tag: list, list of tuple, containing (text, POS tag and class)
        [('Department', 'PROPN', 'department'),
         ('of', 'ADP', 'department'),
         ...
         ('Taiwan', 'PROPN', 'institution')
        ]
    """
    token_tag = []
    parsed = parse_affil(affiliation_text)
    department = parsed['department']
    institution = parsed['institution']
    location = parsed['location'].replace('Electronic address:', '').strip()
    country = parsed['country']
    email = parsed['email']
    for token in nlp(affiliation_text):
        if token.text.lower() in department.lower():
            token_tag.append((token.text, 'department'))
        elif token.text.lower() in institution.lower():
            token_tag.append((token.text, 'institution'))
        elif token.text.lower() in location.lower():
            token_tag.append((token.text, 'location'))
        elif token.text.lower() in country.lower():
            token_tag.append((token.text, 'country'))
        elif token.text.lower() in email.lower():
            token_tag.append((token.text, 'email'))
        else:
            token_tag.append((token.text, 'unknown'))
    token_pos = nlp(' '.join(t[0] for t in tokens))
    token_tag = [(x1[0], x2, x1[1]) for (x1, x2) in zip(token_tag, [t.pos_ for t in token_pos])]
    return token_tag

def affils2token(affiliations):
    """
    Sample affiliations from MEDLINE, tag it using rule-based
    rule-based affiliation parser
    """
    tokens_tag = []
    for affiliation_text in affiliations:
        token_tag = affil2token(affiliation_text)
        tokens_tag.append(token_tag)
    return tokens_tag

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
    return features

def token2features(sent):
    """
    plain text to token
    """
    return [word2features(sent, i) for i in range(len(sent))]

def sent2features(sent):
    return token2features(affil2token(sent))

def sent2labels(sent):
    return [label for (token, postag, label) in sent]

def train(tokens_tag, model_name='affil_parser.crfsuite'):
    """
    Training
    """
    X_train = [sent2features(s) for s in tokens_tag]
    y_train = [sent2labels(s) for s in tokens_tag]

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0, # l1 penalty
        'c2': 1e-3, # l2 penalty
        'max_iterations': 50,  # stop earlier
        'feature.possible_transitions': True
    })
    # train model
    trainer.train(model_name)

def load_train(model_name='affil_parser.crfsuite'):
    """
    Usage example: tagger.tag(sent2features(affiliation_text))
    """
    tagger = pycrfsuite.Tagger()
    tagger.open(model_name)
    return tagger
