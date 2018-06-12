This directory contains the datasets, one of which, `advising`, is new, while the others are modified forms of data from prior work.
Our changes included:

- Canonicalisation of SQL and storage format
- Fixing errors
- Identifying variables

# Files

For each dataset we provide:

- `*.json`, the questions and corresponding queries
- `*-db.sql`, the database
- `*-fields.txt`, a list of fields in the database
- `*-schema.csv`, key information about each database field

For four of the databases are not included either for size or licensing reasons.
They can be found:

Dataset  | Database
-------- | ----------
Academic | TODO
IMDB     | TODO
Scholar  | TODO
Yelp     | TODO

# Format



- Note multiple SQL in some cases. We used the first one in our experiments.

# Other content

The two directories contain relevant data that we did not use in our paper:

- `non-sql-data`, variants of the datasets (e.g. with logical forms instead of SQL, or with translation into other languages)
- `original`, the data from prior work that we modified


