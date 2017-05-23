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

## Training dataset

We obtained 190k parsed affiliations string in following format

```python
<aff xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
  <institution>Department of Emergency Medicine Hennepin County Medical Center</institution>
  <addr-line>Minneapolis, MN</addr-line>
</aff>
```

from Pubmed Open-Access subset using [pubmed_parser](https://github.com/titipata/pubmed_parser).
We did some preprocessing to make it into tokens in `(text, postag, label)` format before training using
Conditional Random Field. Example of the training is as follows.

```python
[('Johns', 'PROPN', 'department'),
 ('Hopkins', 'PROPN', 'department'),
 ('University', 'PROPN', 'department'),
 ('Applied', 'PROPN', 'department'),
 ('Physics', 'PROPN', 'department'),
 ('Laboratory', 'PROPN', 'department'),
 (',', 'PUNCT', 'unknown'),
 ('Laurel', 'PROPN', 'addr-line'),
 (',', 'PUNCT', 'unknown'),
 ('MD', 'PROPN', 'addr-line'),
 (',', 'PUNCT', 'unknown'),
 ('USA', 'PROPN', 'country')]
```

We also made the dataset available in JSON format [here](https://s3-us-west-2.amazonaws.com/affilparser/training_affiliation.json).


## Requirements

- [pycrfsuite](https://github.com/scrapinghub/python-crfsuite)
- [spacy](https://spacy.io/) with English corpus


## Citation

If you use this package, please cite it like this

> Titipat Achakulvisut, Daniel E. Acuna (2017) "Affiliation Parser" https://github.com/titipata/affilparser
