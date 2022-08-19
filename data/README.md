This directory contains the datasets, one of which, `advising`, is new, while the others are modified forms of data from prior work.
Our changes included:

- Canonicalisation of SQL and storage format
- Fixing errors
- Identifying variables

# Files

For each dataset we provide:

- `*.json`, the questions and corresponding queries
- `*-db.sql` or `*-db.txt`, the database in the form it was available
- `*-db.sqlite`, (untested) an sqlite version of the database, generated in 2020 using <https://gist.github.com/esperlu/943776>
- `*-fields.txt`, a list of fields in the database
- `*-schema.csv`, key information about each database field

Some of the databases are not included in the repository.
They can be found as follows (the alternative locations have been added with permission from the authors of the original papers, please remember to cite their work if you use their data):

Dataset  | Database
-------- | ----------
Academic (MAS), IMDB, Yelp | <https://drive.google.com/drive/folders/0B-2uoWxAwJGKY09kaEtTZU1nTWM> or <https://unisyd-my.sharepoint.com/:u:/g/personal/jonathan_kummerfeld_sydney_edu_au/EZKSPtcxPW9PvodZ-DzYn6YB1bsbREHh2Q5APcqWLOnMeQ?e=Hx0CiU>
Scholar  | <https://drive.google.com/file/d/0Bw5kFkY8RRXYRXdYYlhfdXRlTVk> or <https://unisyd-my.sharepoint.com/:u:/g/personal/jonathan_kummerfeld_sydney_edu_au/ERF1m9xu-NFBs1FMg-YkXFQBbwh6amWjLtSFEHVyXV11QA?e=kYZ3J6>
Spider   | <https://yale-lily.github.io/spider>

For more information about the sources of data see the [READ-history.md](./READ-history.md) file.

## Evaluation data split definition

Question split - Where possible, we follow the divisions from prior work.

Query split - Random assignment (note that this did not take into consideration the number of questions for a given query).

For the smaller datasets, we use cross-validation (randomly assigned) and provide our split definitions to enable exact replication.

For the larger datasets, at test time we train on both the training and development sets.

# Format

Each json file contains a list of queries with the following fields:

Symbol             | Type              | Meaning
------------------ | ----------------- | -----------------------------
query-split        | string            | Whether this is a training, development or test query [large datasets] or the split number for 10-fold cross validation [small datasets]
sentences          | list of mappings  | -
sentences/question-split | string            | Whether this is a training, development or test question [large datasets] or the split number for 10-fold cross validation [small datasets]
sentences/text           | string            | The text of the question, with variable names
sentences/variables      | mapping           | Mapping from variable names to values
sql                | list of strings   | SQL queries with variable names. Note - we only use the first query, but retain the variants for completeness (e.g. using joins vs. conditions).
variables          | list of mappings  | -
variables/location       | string            | Whether this occurs in the SQL only, the question only, or both
variables/example        | string            | An example value that could fill the variable (in the SQL only case, this is what is used)
variables/name           | string            | The variable name
variables/type           | string            | Dataset specific type

For WikiSQL and Spider we have a few additional fields:

Symbol             | Type              | Meaning
------------------ | ----------------- | -----------------------------
sentences/original | string            | The question from the original dataset, before our simple tokenisation
sentences/database | string            | The name of the database this question is for [Spider]
sentences/table-id | string            | The name of the table this question is for [WikiSQL]
sql-original       | list of strings   | The query from the original dataset, before our canonicalisation

Also, there are a few caveats:

- There is no query split.
- For Spider the test set is currently not available here (it is being kept secret by the original creators).
- We did automatic variable identification and spot checked some of it (if you find issues, let us know!).
- We modified our canonicalisation script to convert the data and spot checked the output (again, if you find issues, let us know!).
- For WikiSQL we substituted in the actual field names, which contain all sorts of characters, so the SQL is not always valid. This substitution also means the 'sql-original' column numbers may be incorrect for some of the examples as we merged based on the final SQL.

Example:

```
{
    "query-split": "test",
    "sentences": [
        {
            "question-split": "train",
            "text": "Is course number0 available to undergrads ?",
            "variables": {
                "department0": "",
                "number0": "519"
            }
        }
    ],
    "sql": [
        "SELECT DISTINCT COURSEalias0.ADVISORY_REQUIREMENT , COURSEalias0.ENFORCED_REQUIREMENT , COURSEalias0.NAME FROM COURSE AS COURSEalias0 WHERE COURSEalias0.DEPARTMENT = \"department0\" AND COURSEalias0.NUMBER = number0 ;"
    ],
    "variables": [
        {
            "example": "EECS",
            "location": "sql-only",
            "name": "department0",
            "type": "department"
        },
        {
            "example": "595",
            "location": "both",
            "name": "number0",
            "type": "number"
        }
    ]
}
```

The schema is formatted as a series of lines, each describing one field from a table:

- Table name
- Field name
- Type
- Null
- Key
- Default
- Extra

When a value is not set (e.g. default) a `-` is used.

# Other content

The two directories contain relevant data that we did not use in our paper:

- `non-sql-data`, variants of the datasets (e.g. with logical forms instead of SQL, or with translation into other languages, from the [GeoQuery](http://www.cs.utexas.edu/users/ml/wasp/) website)
- `original`, the data from prior work that we modified

