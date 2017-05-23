import re
import spacy
from keywords import DEPARTMENT, INSTITUTE

nlp = spacy.load('en')

def split_affil_tuple(affil_tuple_input):
    affil_tuple = []
    for (tag, affil_text) in affil_tuple_input:
        if ', ' in affil_text:
            for affil_split in affil_text.split(', '):
                affil_tuple.append((tag, affil_split))
        else:
            affil_tuple.append((tag, affil_text))
    return affil_tuple

def re_tag_affil_tuple(affil_tuple_input):
    """
    Re-tag affiliation tuple,
    """
    affiliation_tuple = []
    for (tag, affil_text) in affil_tuple_input:
        if any([t in affil_text for t in DEPARTMENT]):
            tag = 'department'
        elif any([t in affil_text.lower() for t in INSTITUTE]):
            tag = 'institution'
        else:
            tag = tag
        affiliation_tuple.append((tag, affil_text))
    return affiliation_tuple


def prepare_crf_tuple(affil_tuple):
    """
    Give an input tuple from Pubmed OA format
    [('institution', 'ORTON Orthopaedic Hospital, Invalid Foundation'),
    ('addr-line', 'Helsinki, MD'),
    ('country', 'USA')]

    Return CRF format training
    """
    affil_tuple_retag = re_tag_affil_tuple(split_affil_tuple(affil_tuple))
    affil_tags = []
    for (tag, affil_text) in affil_tuple_retag:
        affil_text = re.sub(',', '', affil_text).strip()
        for w in affil_text.split():
            if any([re.match(e, affil_text) for e in EMAIL]):
                affil_tags.append(('email', w))
            elif any([re.match(e, affil_text) for e in ZIP_CODE]) and tag == 'addr-line':
                if '-' in w:
                    for t in nlp(w):
                        affil_tags.append(('zipcode', t.text))
                else:
                    affil_tags.append(('zipcode', w))
            else:
                affil_tags.append((tag, w))
        affil_tags.append(('unknown', ','))
    return affil_tags


def tag_pos_token(tokens):
    """
    Tag part-of-speech to given token
    """
    tokens_out = []
    affil_text = ' '.join([text for label, text in tokens])
    labels = [label for label, text in tokens]
    tokens_tag = [(t.text, t.pos_) for t in nlp(affil_text)]
    if len(tokens_tag) == len(tokens):
        for (text, postag), label in zip(tokens_tag, labels):
            tokens_out.append((text, postag, label))
    return tokens_out
