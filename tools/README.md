These are useful tools for processing the SQL data.

### canonicaliser.py

This is the code we wrote to modify SQL to have a consistent style, specifically:

- Tokenisation, e.g. each bracket is a separate token, except when used as part of COUNT, MAX, etc
- Case, all keywords are uppercase, while variable names are lowercase
- Aliases, converted to be of the form `TABLEaliasN`, where `TABLE` is the name of a table and `N` is a number
- Order, conditionals are ordered alphabetically, and the two sides of the conditional are also ordered

Tests were developed in the process of developing the code and are also included.
If you do use this we would suggest proceeding with care - if your SQL contains phenomena we had not considered then the results could be unexpected.

### corpus_stats.py

Collects a few simple statistics about a dataset:

- Number of questions
- Number of queries
- Number of selects per query
- Query depth (nesting)
- Query breadth (multiple selects at the same level)

### json_to_flat.py

A convenient tool to convert from our json format to three files (train, dev, test) conaining one example per line: `sentence | query` with variables filled in.

### reformat_text2sql_data.py

A utility script to write json formatted datasets split by question/query splits and also divided by train/dev/test or cross validation splits.
This helps read in data independently and simplifies the data loading process.

