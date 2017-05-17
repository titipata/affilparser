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

def affil2token(affiliation_text, tag=True):
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
    if tag:
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
    else:
        for token in nlp(affiliation_text):
            token_tag.append((token.text, token.pos_))
    return token_tag

def affils2token(affiliations):
    """
    Sample affiliations from MEDLINE, tag it using rule-based
    rule-based affiliation parser
    """
    tokens_all = []
    for affiliation_text in affiliations:
        tokens = affil2token(affiliation_text)
        tokens_all.append(tokens)
    return tokens_all

def word2features(tokens, i):
    word, postag = tokens[i][0], tokens[i][1]
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
        word1, postag1 = tokens[i-1][0], tokens[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')

    if i < len(tokens) - 1:
        word1, postag1 = tokens[i+1][0], tokens[i+1][1]
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

def token2features(tokens):
    return [word2features(tokens, i) for i in range(len(tokens))]

def sent2features(sent):
    return token2features(affil2token(sent))

def token2labels(tokens):
    return [label for (token, postag, label) in tokens]

def token2json(tokens):
    """
    Aim for saving training tokens to json format
    """
    tokens_json = []
    for token in tokens:
        tokens_json.append({'text': token[0],
                            'postag': token[1],
                            'class': token[2]})
    return tokens_json # save this later as training set

def json2token(tokens_json):
    tokens = []
    for token in tokens_json:
        tokens.append((token['text'],
                       token['postag'],
                       token['class']))
    return tokens

def train(tokens_all, model_name='affil_parser.crfsuite'):
    """
    Training
    """
    X_train = [token2features(tokens) for tokens in tokens_all]
    y_train = [token2labels(tokens) for tokens in tokens_all]

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
