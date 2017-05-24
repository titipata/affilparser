import os
import re
import spacy
import pycrfsuite
from itertools import groupby, product, chain
from .keywords import EMAIL, ZIP_CODE, COUNTRY, UNIVERSITY_ABBR, DEPARTMENT, STREET

nlp = spacy.load('en')
MODEL_PATH = os.path.join('model', 'affilparser.crfsuite')

class AffiliationParser(object):
    """AffiliationParser

    Conditional Random Field parser for MEDLINE/Pubmed
    affiliation string
    """
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
            elif (text.isdigit() and len(text) != 5) or text in STREET or (tag == 'zipcode' and not text.isdigit()):
                predictions_correct.append((text, 'addr-line'))
            elif any([re.match(e, text) for e in ZIP_CODE]) or (text.isdigit() and len(text) == 5):
                predictions_correct.append((text, 'zipcode'))
            else:
                predictions_correct.append((text, tag))
        return predictions_correct

    def chunk_address(self, predictions):
        predictions_chunk = []
        predictions_zip = list(zip(predictions, predictions[1:] + [('', '')], predictions[2:] + 2 * [('', '')]))
        i = 0
        while i <= len(predictions) - 1:
            (text, pred), (text1, pred1), (text2, pred2) = predictions_zip[i]
            if text.isdigit() and text1 == '-' and text2.isdigit():
                predictions_chunk.append((text + text1 + text2, pred))
                i += 3
            else:
                predictions_chunk.append((text, pred))
                i += 1
        return predictions_chunk

    def chunk_zipcode(self, predictions):
        predictions_chunk = []
        predictions_zip = list(zip(predictions, predictions[1:] + [('', '')], predictions[2:] + 2 * [('', '')]))
        i = 0
        while i <= len(predictions) - 1:
            (text, pred), (text1, pred1), (text2, pred2) = predictions_zip[i]
            if pred == 'addr-line' and pred1 == 'zipcode' and pred2 == 'addr-line':
                predictions_chunk.append((text, pred))
                predictions_chunk.append((text1, 'addr-line'))
                i += 2
            else:
                predictions_chunk.append((text, pred))
                i += 1
        return predictions_chunk

    def correct_chunk_prediction(self, predictions):
        predictions_correct = []
        for (text, tag) in predictions:
            if any([e in text for e in DEPARTMENT]):
                predictions_correct.append((text, 'department'))
            elif any([e in text.lower() for e in UNIVERSITY_ABBR]):
                predictions_correct.append((text, 'institution'))
            else:
                predictions_correct.append((text, tag))
        return predictions_correct

    def chunk_prediction(self, predictions):
        return [(' '.join([g_[0] for g_ in g]).strip(), tag)
                for tag, g in groupby(predictions, lambda x: x[1])]

    def separate_prediction(self, predictions_chunk):
        """
        Chunking output in case there are more than one affiliations
        """
        predictions_rm = [(text, tag) for (text, tag) in predictions_chunk if not tag in ('unknown', 'bold')]
        sep = []
        r_prev = 0
        for r, ((text1, tag1), (text2, tag2)) in enumerate(zip(predictions_rm, predictions_rm[1:] + [('', '')])):
            for t1, t2 in product(['addr-line', 'country', 'zipcode', 'email'], ['department']):
                if tag1 == t1 and tag2 == t2:
                    sep.append((r_prev, r + 1))
                    r_prev = r + 1
        sep.append((r_prev, len(predictions_rm)))
        if len(sep) > 1:
            prediction_sep = []
            index = 0
            for start, end in sep:
                prediction_sep += predictions_rm[index:start]
                prediction_sep.append(predictions_rm[start:end])
                index = end
        else:
            prediction_sep = predictions_rm
        return prediction_sep

    def parse(self, text):
        tokens = self.text2token(text)
        word_features = self.token2features(tokens)
        tags_pred = self.tagger.tag(word_features)
        zip_pred = list(zip(tokens, tags_pred))
        predictions = [(text, pred) for (text, postag), pred in zip_pred]
        predictions = self.chunk_address(predictions)
        predictions = self.correct_prediction(predictions)
        predictions = self.chunk_zipcode(predictions)
        predictions_chunk = self.chunk_prediction(predictions)
        predictions_chunk = self.correct_chunk_prediction(predictions_chunk)
        prediction_sep = self.separate_prediction(predictions_chunk)
        if any(isinstance(e, list) for e in prediction_sep):
            prediction_sep = [self.chunk_prediction(pred) for pred in prediction_sep]
            prediction_sep_merge = list(chain.from_iterable(prediction_sep))
            if len(prediction_sep_merge) <= 4:
                prediction_sep = prediction_sep_merge
        else:
            prediction_sep = self.chunk_prediction(prediction_sep)
        return prediction_sep
