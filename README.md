# Affiliation Parser

Python Conditional Random Field (CRF) Parser for Affiliation String in MEDLINE and Pubmed OA.


## Example

We implement the parser using [python-crfsuite](https://github.com/scrapinghub/python-crfsuite).
See this [example](https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb)
on how to implement.

```python
from affilparser import AffiliationParser

text = """
  Department of Agricultural and Biosystems Engineering, Iowa State University, Ames, IA 50011-3080, USA;
  Department of Energy, Power Engineering and Environment, Faculty of Mechanical Engineering and Naval Architecture, University of Zagreb, Ivana Lucica 5, HR-10000 Zagreb, Croatia;
  Department of Civil, Construction and Environmental Engineering, Iowa State University, Ames, IA 50011-3232, USA.
"""

parser = AffiliationParser()
parsed_affil = parser.parse(text)
```


## Requirements

- [pycrfsuite](https://github.com/scrapinghub/python-crfsuite)
- [spacy](https://spacy.io/) with English corpus
