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
        elif ';' in affil:
            affiliations.extend([a_ for a_ in affil.split(';')])
        else:
            affiliations.append(affil)
    affiliations = pd.unique(affiliations)
    for affil in affiliations:
        affiliations_split.extend(affil.split('; '))
    affiliations_unique = pd.unique(affiliations_split)
    return affiliations_unique


if __name__ == '__main__':
    medline_df = spark.read.parquet('raw_medline.parquet') # parsed using pubmed_parser
    affiliation_df = medline_df[['pmid', 'affiliation']].filter("affiliation != ''")
    affiliation_sample = affiliation_df.sample(False, fraction=0.1) # sample from full
    affiliation_df = affiliation_sample.toPandas()
    affiliations_unique = get_unique_affiliation(affiliation_pandas.affiliation)
    affiliations_eval = pd.DataFrame(affiliations_unique, columns=['affiliation']).sample(n=1200, random_state=10)
    affiliations_eval.to_csv('affiliation_eval.csv', index=False)
