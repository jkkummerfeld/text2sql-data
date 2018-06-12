# text2sql-data
This repository contains data and code for building and evaluating systems that map sentences to SQL.
For a range of domains, we provide:

- Sentences with annotated variables
- SQL queries
- A database schema
- A database

Version | Description
------- | -------------
1       | Data used in the ACL 2018 paper

TODO: codalab

# Using the data

If you use this data in your work, please cite our ACL paper *and* the appropriate original sources, and list the version number of the data:

```TeX
@InProceedings{data-sql-advising,
  author    = {Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev},
  title     = {Improving Text-to-SQL Evaluation Methodology},
  booktitle = {Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  shortvenue = {ACL},
  month     = {July},
  year      = {2018},
  address   = {Melbourne, Victoria, Australia},
  pages     = {},
  url       = {},
}

@InProceedings{data-sql-imdb-yelp,
  dataset   = {IMDB and Yelp},
  author    = {Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and Thomas Dillig},
  title     = {SQLizer: Query Synthesis from Natural Language},
  booktitle = {International Conference on Object-Oriented Programming, Systems, Languages, and Applications, ACM},
  year      = {2017},
  pages     = {},
  url       = {},
}
```

Example citation:

```
In this work, we use the modified SQL datasets from \citet{data-advising} version 1, based on \citet{data-academic,data-atis-original,data-geography-original,data-atis-geography-scholar,data-imdb-yelp}
```

If you are only using one dataset, here are example ciwtation commands:

Data         | Cite
------------ | ------
Academic     | `\citet{data-advising,data-academic}`
Advising     | `\citet{data-advising}`
ATIS         | `\citet{data-advising,data-atis-original,data-atis-geography-scholar}`
Geography    | `\citet{data-advising,data-geography-original,data-atis-geography-scholar}`
Restaurants  | TODO `\citet{data-advising,}`
Scholar      | `\citet{data-advising,data-atis-geography-scholar}`
IMDB         | `\citet{data-advising,data-imdb-yelp}`
Yelp         | `\citet{data-advising,data-imdb-yelp}`

# Contributions

We put substantial effort into fixing bugs in the datasets, but none of them are perfect.
If you find a bug, please submit a pull request with a fix.
We will be merging fixes into a development branch and only infrequently merging all of those changes into the master branch (at which point this page will be adjusted to note that it is a new release).
This approach is intended to balance the need for clear comparisons between systems, while also improving the data.

# Format 

See `data/README.md` for details on our format.
