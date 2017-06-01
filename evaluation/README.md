# Evaluation

This folder contains sample 1200 affiliation strings (`affiliations_medline.csv`)
randomly sampled from Medline affiliation strings parsed using
[pubmed_parser](https://github.com/titipata/pubmed_parser).


## Performance on [Grobid dataset](https://github.com/kermitt2/grobid)

From the root of the repository, run

```python
python evaluation/evaluate.py
```

and you should see the following results:


```bash
            precision     recall      f1-score      support

address     0.712         0.623       0.664         602
department  0.734         0.775       0.754         1953
city        0.632         0.659       0.645         443
institution 0.685         0.700       0.692         1937
postal_box  0.891         0.781       0.832         73
postal_code 0.853         0.857       0.855         203
country     0.930         0.913       0.922         450
state       0.838         0.779       0.807         172

avg / total 0.732         0.739       0.735         5833
```

## Speed Performance

Here, we show the speed performance of parser per given string with
varies tokens length.

<img src="time_performance.png" width="400" />
