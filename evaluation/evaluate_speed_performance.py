import pandas as pd
import time
import spacy
from altair import *
from altair import Chart, load_dataset
nlp = spacy.load('en')

def timed(text):
    ts = time.time()
    parser.parse(text)
    te = time.time()
    result = te - ts
    return result


if __name__ == '__main__':
    affiliations = pd.read_csv('affiliation.csv') # CSV of affiliations in
    affiliations = list(affiliations.affiliation)
    affiliations_len = [(affiliation, len([t for t in nlp(affiliation)]))
                        for affiliation in affiliations]
    affiliations_len_df = pd.DataFrame(affiliations_len, columns=['affiliation', 'n_token'])
    affiliations_len_filter_df = affiliations_len_df.sort_values('n_token', ascending=True).query("n_token > 10").query("n_token < 50")
    affiliations_len_filter_df['time'] = affiliations_len_filter_df.affiliation.map(lambda x: timed(x))
    runtime_df = affiliations_len_filter_df[['n_token', 'time']].groupby('n_token').mean().reset_index()

    chart = Chart(runtime_df).mark_circle().encode(
        x=X('n_token', scale=Scale(domain=(10, 50)), title='Number of Tokens'),
        y=Y('time', scale=Scale(domain=(0.0, 5.0)), title='Time (ms)'),
    ).configure_facet_cell(
        strokeWidth=0.0,
    )
