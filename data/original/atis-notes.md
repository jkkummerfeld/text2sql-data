The original UW files were processed as follows:

1. Combined into single files:
paste $name.nl $name.sql | sed $'s/\t/ ||| /' > atis.uw.$name.sql.no-vars.question-split.txt

Bugfixing:
- Incorrect use of DAILY
- Incorrect inclusion of airline constraints
- Incorrect handling of Dallas Fort Worth
- Other minor bugs

2. Canonicalised:
for name in train dev test ; do
  echo "atis.uw.$name.sql.no-vars.question-split.txt" | ../../tools/canonicaliser.py --fields ../fields-atis.txt --nonjson
  mv atis.uw.$name.sql.no-vars.question-split.txt.canonical.json atis.uw.$name.sql.no-vars.question-split.canon
done

3. Add variables:
tools/combine-queries.py --train atis.uw.train.sql.no-vars.question-split.canon --test atis.uw.test.sql.no-vars.question-split.canon --dev atis.uw.dev.sql.no-vars.question-split.canon > atis.vars.squestion-split.json

Variable issues that we did not resolve, for these the sentence is left as is, but the variable is given so that the SQL can be filled in:

- Evening flights extending into the next day, e.g. "Friday evening" includes "Saturday early morning" in queries
- Times that are 'around' some time or 'in the morning' are left as is
- Class types
- When 'weekdays' are referred to
- States that are used when only their city is mentioned

Note - this means variables are NOT simply changeable in this data (unlike the advising data)

4. Manual post processing:

- Bugfes from our variable detection when a word is used twice to refer to different things (e.g. a city and an airport, or a month and a time)
- Dealt with duplicate queries (for ambiguities, e.g. 'between', we followed examples from the data for interpretation)

## Known remaining issues:

- Consistency on the use of '<' or '<='
- Look at any case where the variables do not occur in the query (some are legitimate, others are not)
- `show me the flights` queries, and other forms of follow ups (running combine-queries with --verbose is helpful)
- `arrival_time < 41` is used all over the place for unknown reasons, typically with `time_elapsed >= 60`. It is often part of repeated query chunks
- "arrive before 5pm on tuesday", is this about any tuesday, or THIS tuesday?
- 'Today' variaes a lot in the data, and a lot of dates are relative to it ('on sunday'), decision - if easy, do it
- Splitting (now that we have merged in deduplication)
- Identify cases of unnecessary brackets, e.g.. ((...))

## Specific examples of issues:

Time not used:
- `i would like to know the flights available from city_name1 to city_name0 arriving in city_name0 by arrival_time0 o'clock wednesday morning`

Missing time in query:
- `show me the earliest flights from city_name0 to city_name1 on wednesday`
- `what airline_code0 flights from city_name1 to city_name0 depart city_name1 after departure_time0 on wednesday`

Incorrect dates for 'thursday' / 'tuesday':
```
21 2 1991 - - - wednesday what are the fares from city_name1 to city_name0 monday and wednesday
21 2 1991 - - - tuesday what flights are available from city_name1 to city_name0 late monday evening or early tuesday morning
23 4 1991 - - - thursday bring up flights from city_name1 to city_name0 on wednesday night or thursday morning
23 4 1991 - - - thursday get last flight from city_name1 to city_name0 on wednesday or first flight from city_name1 to city_name0 on thursday
23 4 1991 - - - thursday i want to fly from city_name1 to city_name0 on either wednesday evening or thursday morning
23 4 1991 - - - thursday i'd like a one way ticket from city_name1 to city_name0 either wednesday evening or thursday morning
23 4 1991 - - - thursday list flights from city_name1 to city_name0 on wednesday afternoon and thursday morning
23 4 1991 - - - thursday please give me flights from city_name1 to city_name0 on wednesday afternoon and thursday morning
23 4 1991 - - - thursday please give me flights from city_name1 to city_name0 on wednesday and thursday
23 4 1991 - - - thursday please give me flights from city_name1 to city_name0 on wednesday morning and thursday afternoon
23 4 1991 - - - thursday show me flights from city_name1 to city_name0 on wednesday night or thursday morning
23 4 1991 - - - thursday show me the flights from city_name1 to city_name0 on wednesday and thursday
23 4 1991 - - - thursday show me the flights from city_name1 to city_name0 on wednesday night and thursday morning
23 4 1991 - - - thursday what flights are there on wednesday evening or thursday morning from city_name0 to airport_code0
23 4 1991 24 - - thursday give me information on flights from city_name1 to city_name0 on wednesday after departure_time1 and thursday before departure_time0
23 4 1991 24 - - thursday i want information on flights from city_name1 to city_name0 i want to leave after departure_time1 on wednesday or before departure_time0 on thursday
23 4 1991 24 - - thursday i want information on flights from city_name1 to city_name0 i want to leave wednesday after departure_time1 or thursday before departure_time0
23 4 1991 24 - - thursday list all flights going from city_name1 to city_name0 after departure_time1 o'clock on wednesday and before departure_time0 o'clock am on thursday
23 4 1991 24 - - thursday please list all of the flights leaving city_name1 heading to city_name0 after departure_time1 wednesday and before departure_time0 thursday
23 4 1991 24 - - thursday show me all the flights from city_name1 to city_name0 that leave after departure_time0 on wednesday and before departure_time1 on thursday
```
