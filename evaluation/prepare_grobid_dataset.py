"""Prepare Grobid dataset for evaluation with our parser.

This script takes a tar.gz file with the XML files of the Grobid project. It
parses the files inside and generates a CSV files with the parsed information.

Grobid project: https://github.com/kermitt2/grobid
"""


import tarfile
from bs4 import BeautifulSoup
import pandas as pd
import re


def parse_affil(affiliation_node):
    def text_or_none(x):
        return x.text if x is not None else None

    institution = affiliation_node.find('orgname', attrs={'type': 'institution'})
    department = affiliation_node.find('orgname', attrs={'type': 'department'})
    postal_code = affiliation_node.find('postcode')
    country = affiliation_node.find('country')
    state = affiliation_node.find('region')
    postal_box = affiliation_node.find('postbox')
    city = affiliation_node.find('settlement')
    address = affiliation_node.find('addrline')
    raw_text = ' '.join(affiliation_node.strings).replace('\n', '').replace('\t', '').strip()
    raw_text = re.sub(' +', ' ', raw_text)
    return {
        'raw_text': raw_text,
        'institution': text_or_none(institution),
        'department': text_or_none(department),
        'postal_code': text_or_none(postal_code),
        'country': text_or_none(country),
        'state': text_or_none(state),
        'postal_box': text_or_none(postal_box),
        'city': text_or_none(city),
        'address': text_or_none(address)
    }


def parse_grobid(tar_gz_path):
    all_affiliations = []
    tf = tarfile.open(tar_gz_path)
    for member in tf.getmembers():
        if member.isfile():
            soup = BeautifulSoup(tf.extractfile(member), 'html.parser')
            for affil_node in soup.findAll('affiliation'):
                parsed = parse_affil(affil_node)
                parsed.update({'file': member.name})
                all_affiliations.append(parsed)
    tf.close()
    return all_affiliations


if __name__ == "__main__":
    grobid_df = pd.DataFrame(parse_grobid('../data/grobid_affiliations.tar.gz'))
    grobid_df.to_csv('affiliations_grobid.csv', index=False)
