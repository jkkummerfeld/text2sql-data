In the process of doing this work a range of issues came up with the data that we did not have time to address.
We are documenting them here for future reference (and in case someone is looking for a way to contribute!).

# ATIS

- The UW data modified the training and development data to avoid nesting, but not the test data. Our de-duplication / merging of queries mean we often have both versions of each query, but in some cases we only have the nested version (if it only appeared in testing).
- Many queries use a date, but nothing is explicitly given in the query. Some say `today`, but the date it corresponds to varies a lot. Others give a day, e.g. `Sunday`, but again the date varies.
- Comparison operators (`<`, `>`, `<=`, etc) are not consistently used. One possible scheme would be `before <`, `after >`, `by <=`, `between >= ... <=`, `around > ... <`, and use `> ... <` for morning, afternoon, and evening ranges.
- Sometimes a variable is specified in the question, but not used in the query, e.g. a time (and vice versa).
- There are queries that only make sense as follow-ups, e.g. `show me the flights`.
- `arrival_time < 41` is used all over the place for unknown reasons, typically with `time_elapsed >= 60`. It is often part of repeated query chunks.
- There is ambiguity in what a day refers to, e.g. does `arrive before 5pm on Tuesday` mean any Tuesday, or THIS Tuesday?

# Advising

- Some paraphrases introduced `I` and `me` in ways that could change the query (e.g. `Which is the easiest MDE course?` vs. `Which is the easiest class I can take to fulfill the requirement0 requirement?`).

# Academic

- Slightly unnatural queries, all starting with `return me` and having a fairly strict sentence structure.

# GeoQuery

- Variables names don't include the type (all are `varN`, but the type is specified in the `variables` data).
- [Logical form] Refers to information that does not exist, e.g. city size.
- [Logical form] Inconsistent use of `US`.
- [Logical form] Treats modifiers inconsistently (e.g. `largest` vs. `largest population` even though we only have population as a measure of size).

# IMDB

- When someone has had multiple jobs (e.g. director and writer) they can be queried in different ways. Really we should treat all people the same and query across all tables about people.

# Restaurants

# Scholar

- There are cases where the `num-cited-by` and `num-citing` fields may simplify the query considerably.
- Possible SQL bugs in:
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

# Yelp

- Some queries reverse `category_name0 category_name1` unnecessarily.

# All

- There are often multiple ways to answer a question in SQL. Some datasets have multiple queries, it would be great to do this more generally (e.g. have nested and join based versions of queries).
