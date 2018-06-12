The original UW files were processed as follows:

1. Combined into single files:

```bash
paste $name.nl $name.sql | sed $'s/\t/ ||| /' > scholar.uw.$name.sql.no-vars.question-split.txt
```

2. Manual Bugfixes:

- Author names that differed between the query and question (query added initials or extra names)
- Inconsistent use of 'this year', or when a year was used when not asked by the question
- Titles of papers that were different (for -> on)
- Incorrect numebrs ("more than 5" but 4 in query)
- Missing constraints, e.g. 'in 2015', '5 most recent'

3. Canonicalised:

```bash
for name in train dev test ; do
  echo "scholar.uw.$name.sql.no-vars.question-split.txt" | ../../tools/canonicaliser.py --fields ../fields-scholar.txt --nonjson
  mv scholar.uw.$name.sql.no-vars.question-split.txt.canonical.json scholar.uw.$name.sql.no-vars.question-split.canon
done
```

4. Add variables:

```bash
tools/combine-queries.py --train scholar.uw.train.sql.no-vars.question-split.canon --test scholar.uw.test.sql.no-vars.question-split.canon --dev scholar.uw.dev.sql.no-vars.question-split.canon > scholar.json
```

5. Manual fixes

- Looking at the vocabulary of questions after introducing variables 
- Identified duplicate queries and merged, listing both SQL statements for now
- Looking for duplicate questions (manually identified similar queries, and also if there is a string match after variables)
- Checked duplicates manually (separate person)
- Additional bugfixes:

## Known issues

The use of cited vs citing, for example:
- ` which venuename0 year0 papers have been cited the most`
- `how many citations does authorname0 have`

Note also that there are fields `non-citing` and `num-cited-by` that could give alternative queries to some in the data now.

Possible SQL bugs in:

```
Which paper should I read about keyphrasename
citation count of authorname0 's papers
who does authorname0 cite
what papers does authorname0 cite
When did authorname0 publish ?
does authorname0 publish a lot ?
topics at venuename0 year0
How many papers did authorname0 co-authored with authorname1
```

