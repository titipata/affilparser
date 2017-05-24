import os
import re
import spacy
import pycrfsuite
from itertools import groupby
from .keywords import EMAIL, ZIP_CODE, COUNTRY

nlp = spacy.load('en')
MODEL_PATH = os.path.join('model', 'affilparser.crfsuite')

class AffiliationParser(object):

    def __init__(self):
        self.tagger = self.load_model(model_name=MODEL_PATH)

    def load_model(self, model_name=MODEL_PATH):
        curdir = os.path.dirname(__file__)
        tagger = pycrfsuite.Tagger()
        tagger.open(os.path.join(curdir, model_name))
        return tagger

    def word2features(self, tokens, i):
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

    def text2token(self, text):
        """
        Give affiliation text, return list of tokens with
        part-of-speech tag
        """
        tokens = []
        for token in nlp(text):
            tokens.append((token.text.strip(), token.pos_))
        return tokens

    def token2features(self, tokens):
        """
        Generate token features for Conditional Random Field
        """
        return [self.word2features(tokens, i) for i in range(len(tokens))]

    def correct_prediction(self, predictions):
        predictions_correct = []
        for (text, tag) in predictions:
            if text in COUNTRY:
                predictions_correct.append((text, 'country'))
            elif any([re.match(e, text) for e in EMAIL]):
                predictions_correct.append((text, 'email'))
            else:
                predictions_correct.append((text, tag))
        return predictions_correct

    def chunk_address(self, predictions):
        predictions_chunk = []
        predictions_zip = list(zip(predictions, predictions[1:] + [('', '')], predictions[2:] + 2 * [('', '')]))
        i = 0
        while i < len(predictions) - 2:
            (text, pred), (text1, pred1), (text2, pred2) = predictions_zip[i]
            if text.isdigit() and text1 == '-' and text2.isdigit():
                predictions_chunk.append((text + text1 + text2, pred))
                i += 3
            else:
                predictions_chunk.append((text, pred))
                i += 1
        return predictions_chunk

    def chunk_prediction(self, predictions):
        return [(' '.join([g_[0] for g_ in g]).strip(), tag)
                for tag, g in groupby(predictions, lambda x: x[1])]

    def parse(self, text):
        tokens = self.text2token(text)
        word_features = self.token2features(tokens)
        tags_pred = self.tagger.tag(word_features)
        zip_pred = list(zip(tokens, tags_pred))
        predictions = [(text, pred) for (text, postag), pred in zip_pred]
        predictions = self.chunk_address(predictions)
        predictions = self.correct_prediction(predictions)
        predictions_chunk = self.chunk_prediction(predictions)
        return predictions_chunk
