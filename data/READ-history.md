# Notes on data sources and history

Summary Table:

Dataset      | Main Paper                                                                  | Data Source
------------ | --------------------------------------------------------------------------- | -----------
academic     | [Li and Jagadish, 2014](http://www.vldb.org/pvldb/vol8/p73-li.pdf)          | Contacted authors
advising     | Finegan-Dollak et al., 2018                                                 | Here!
atis         | [Iyer et al., 2017](http://aclweb.org/anthology/P/P17/P17-1089.pdf)         | [UW](https://github.com/sriniiyer/nl2sql/tree/master/data)
geography    | [Iyer et al., 2017](http://aclweb.org/anthology/P/P17/P17-1089.pdf)         | [UW](https://github.com/sriniiyer/nl2sql/tree/master/data)
imdb         | [Yaghmazadeh et al., 2017](http://doi.org/10.1145/3133887)                  | [UT](https://drive.google.com/drive/folders/0B-2uoWxAwJGKY09kaEtTZU1nTWM)
restaurants  | [Popescu et al., 2003](https://doi.org/10.1007/978-3-642-45260-4_5)         | [Trento](https://ikernels-portal.disi.unitn.it/repository/semmap/)
scholar      | [Iyer et al., 2017](http://aclweb.org/anthology/P/P17/P17-1089.pdf)         | [UW](https://github.com/sriniiyer/nl2sql/tree/master/data)
yelp         | [Yaghmazadeh et al., 2017](http://doi.org/10.1145/3133887)                  | [UT](https://drive.google.com/drive/folders/0B-2uoWxAwJGKY09kaEtTZU1nTWM)

## academic

Created for NaLIR by enumerating all of the different queries possible with the Microsoft Academic Search interface, then writing questions for each query.

## advising

1. Collected questions from Facebook and undergraduates (past CLAIR lab students), then wrote further questions of a similar style.
2. Four people wrote SQL queries for all of the questions (one per question).
3. Six people scored the queries for helpfulness and accuracy (two people per query).
4. Collected paraphrases on Mechanical Turk, then one person checked them all, correcting/filtering for major grammatical or correctness issues and adding paraphrases to stay above a minimum of 10 per query.

The default student is in EECS (needed for assumed content of queries).
In the database they are represented by student record ID 1.

## atis

1. Originally collected for the "The ATIS spoken language systems pilot corpus"
2. Modified by Iyer et al. to reduce nesting.

## geoquery

1. Originally a dataset created at UT Austin with sentences and logical forms.
2. Prolog converted to SQL at UW in the early 2000s.
3. Further queries converted and SQL improved at the University of Trento.
4. 2017 UW paper uses the earlier UW work with additions to cover the remaining queries.

We have corrected some minor issues in the data:

- References to population density of cities, which is not in the database
- Inconsistent handling of rivers
- Inconsistent use of either sorting or a subquery for questions that ask for the max of something
- Use of 'US' in various ways that are inconsistent

## restaurants

1. Originally a dataset created at UT Austin with sentences and logical forms.
2. Converted to SQL by Popescu et al. (UW)
3. Improved by Giordani and Moschitti (Trento)

## scholar

Constructed at UW in 2017

## yelp and imdb

Constructed at UT Austin in 2017

Note - in the imdb dataset there are some cases where multiple SQL queries are provided because of ambiguity in the question. For example:

```
"What is the nationality of Ben Affleck?"
"select director_0.nationality from director as director_0 where director_0.name = \" Ben Affleck \" "
"select actor_0.nationality from actor as actor_0 where actor_0.name = \" Ben Affleck \" "
```

