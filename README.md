# Affiliation Parser

This is a repository where we use ML algorithm for affiliation parser.

## Conditional Random Field (CRF)

See this [example](https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb) on
how to implement using [python-crfsuite](https://github.com/scrapinghub/python-crfsuite)

```python
import pycrfsuite
from crf_utils import affil2token, token2features

text = """
  Department of Agricultural and Biosystems Engineering, Iowa State University, Ames, IA 50011-3080, USA;
  Department of Energy, Power Engineering and Environment, Faculty of Mechanical Engineering and Naval Architecture, University of Zagreb, Ivana Lucica 5, HR-10000 Zagreb, Croatia;
  Department of Civil, Construction and Environmental Engineering, Iowa State University, Ames, IA 50011-3232, USA.
"""

tagger = pycrfsuite.Tagger()
tagger.open('model/affil_parser.crfsuite')
token_tag = affil2token(text, tag=False)
predictions = tagger.tag(token2features(token_tag))
token_predictions = list(zip(token_tag, predictions)) # output
```


## Requirements

- [pycrfsuite](https://github.com/scrapinghub/python-crfsuite)
- [spacy](https://spacy.io/)
- [affiliation_parser](https://github.com/titipata/affiliation_parser)
