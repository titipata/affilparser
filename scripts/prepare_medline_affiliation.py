import pandas as pd

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
