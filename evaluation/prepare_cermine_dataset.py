import pandas as pd
import requests


if __name__ == '__main__':
    affiliations_df = pd.read_csv('affiliations_medline.csv', header=None)
    affiliations = list(affiliations_df[0])

    parsed_affiliations = []
    for affiliation in affiliations:
        r = requests.post('http://cermine.ceon.pl/parse.do', data={'affiliation' : affiliation})
        parsed_affiliations.append(r.text)

    df = pd.DataFrame(list(zip(affiliations, parsed_affiliations)), columns=['affiliation', 'cermine_parsed'])
    df.to_csv('../data/cermine_affiliations.csv', index=False)
