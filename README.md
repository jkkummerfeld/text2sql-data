# text2sql-data
This repository contains data and code for building and evaluating systems that map sentences to SQL, developed as part of:

  - [Improving Text-to-SQL Evaluation Methodology](http://aclweb.org/anthology/P18-1033),
  Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev,
  ACL 2018

For a range of domains, we provide:

- Sentences with annotated variables
- SQL queries
- A database schema
- A database

These are improved forms of prior datasets and a new dataset we developed.
We have separate files describing the [datasets](./data/), [systems](./systems/), and [tools](./tools/).

Version | Description
------- | -------------
2       | Data with fixes for variables incorrectly defined in questions
1       | Data used in the ACL 2018 paper

# Citing this work

If you use this data in your work, please cite our ACL paper _and_ the appropriate original sources, and list the version number of the data.
For example, in your paper you could write (using the BibTeX below):

```
In this work, we use version 1 of the modified SQL datasets from \citet{data-advising}, based on \citet{data-academic,data-atis-original,data-geography-original,data-atis-geography-scholar,data-imdb-yelp,data-restaurants-logic,data-restaurants-original,data-restaurants}
```

If you are only using one dataset, here are example citation commands:

Data         | Cite
------------ | ------
Academic     | `\citet{data-advising,data-academic}`
Advising     | `\citet{data-advising}`
ATIS         | `\citet{data-advising,data-atis-original,data-atis-geography-scholar}`
Geography    | `\citet{data-advising,data-geography-original,data-atis-geography-scholar}`
Restaurants  | `\citet{data-advising,data-restaurants-logic,data-restaurants-original,data-restaurants}`
Scholar      | `\citet{data-advising,data-atis-geography-scholar}`
IMDB         | `\citet{data-advising,data-imdb-yelp}`
Yelp         | `\citet{data-advising,data-imdb-yelp}`

```TeX
@InProceedings{data-sql-advising,
  dataset   = {Advising},
  author    = {Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev},
  title     = {Improving Text-to-SQL Evaluation Methodology},
  booktitle = {Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  month     = {July},
  year      = {2018},
  location  = {Melbourne, Victoria, Australia},
  pages     = {351--360},
  url       = {http://aclweb.org/anthology/P18-1033},
}

@InProceedings{data-sql-imdb-yelp,
  dataset   = {IMDB and Yelp},
  author    = {Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and Thomas Dillig},
  title     = {SQLizer: Query Synthesis from Natural Language},
  booktitle = {International Conference on Object-Oriented Programming, Systems, Languages, and Applications, ACM},
  month     = {October},
  year      = {2017},
  pages     = {63:1--63:26},
  url       = {http://doi.org/10.1145/3133887},
}

@article{data-academic,
  dataset   = {Academic},
  author    = {Fei Li and H. V. Jagadish},
  title     = {Constructing an Interactive Natural Language Interface for Relational Databases},
  journal   = {Proceedings of the VLDB Endowment},
  volume    = {8},
  number    = {1},
  month     = {September},
  year      = {2014},
  pages     = {73--84},
  url       = {http://dx.doi.org/10.14778/2735461.2735468},
} 

@InProceedings{data-atis-geography-scholar,
  dataset   = {Scholar, and Updated ATIS and Geography},
  author    = {Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, Jayant Krishnamurthy, and Luke Zettlemoyer},
  title     = {Learning a Neural Semantic Parser from User Feedback},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2017},
  pages     = {963--973},
  location  = {Vancouver, Canada},
  url       = {http://www.aclweb.org/anthology/P17-1089},
}

@article{data-atis-original,
  dataset   = {ATIS, original},
  author    = {Deborah A. Dahl, Madeleine Bates, Michael Brown, William Fisher, Kate Hunicke-Smith, David Pallett, Christine Pao, Alexander Rudnicky, and Elizabeth Shriber},
  title     = {{Expanding the scope of the ATIS task: The ATIS-3 corpus}},
  journal   = {Proceedings of the workshop on Human Language Technology},
  year      = {1994},
  pages     = {43--48},
  url       = {http://dl.acm.org/citation.cfm?id=1075823},
}

@inproceedings{data-geography-original
  dataset   = {Geography, original},
  author    = {John M. Zelle and Raymond J. Mooney},
  title     = {Learning to Parse Database Queries Using Inductive Logic Programming},
  booktitle = {Proceedings of the Thirteenth National Conference on Artificial Intelligence - Volume 2},
  year      = {1996},
  pages     = {1050--1055},
  location  = {Portland, Oregon},
  url       = {http://dl.acm.org/citation.cfm?id=1864519.1864543},
}

@inproceedings{data-restaurants-logic,
  author    = {Lappoon R. Tang and Raymond J. Mooney},
  title     = {Automated Construction of Database Interfaces: Intergrating Statistical and Relational Learning for Semantic Parsing},
  booktitle = {2000 Joint SIGDAT Conference on Empirical Methods in Natural Language Processing and Very Large Corpora},
  year      = {2000},
  pages     = {133--141},
  location  = {Hong Kong, China},
  url       = {http://www.aclweb.org/anthology/W00-1317},
}

@inproceedings{data-restaurants-original,
 author    = {Ana-Maria Popescu, Oren Etzioni, and Henry Kautz},
 title     = {Towards a Theory of Natural Language Interfaces to Databases},
 booktitle = {Proceedings of the 8th International Conference on Intelligent User Interfaces},
 year      = {2003},
 location  = {Miami, Florida, USA},
 pages     = {149--157},
 url       = {http://doi.acm.org/10.1145/604045.604070},
}

@inproceedings{data-restaurants,
  author    = {Alessandra Giordani and Alessandro Moschitti},
  title     = {Automatic Generation and Reranking of SQL-derived Answers to NL Questions},
  booktitle = {Proceedings of the Second International Conference on Trustworthy Eternal Systems via Evolving Software, Data and Knowledge},
  year      = {2012},
  location  = {Montpellier, France},
  pages     = {59--76},
  url       = {https://doi.org/10.1007/978-3-642-45260-4_5},
}
```

# Contributions

We put substantial effort into fixing bugs in the datasets, but none of them are perfect.
If you find a bug, please submit a pull request with a fix.
We will be merging fixes into a development branch and only infrequently merging all of those changes into the master branch (at which point this page will be adjusted to note that it is a new release).
This approach is intended to balance the need for clear comparisons between systems, while also improving the data.

# Acknowledgments

This material is based in part upon work supported by IBM under contract 4915012629. Any opinions, findings, conclusions or recommendations expressed are those of the authors and do not necessarily reflect the views of IBM.
