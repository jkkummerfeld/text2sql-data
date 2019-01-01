#!/usr/bin/env bash

export S2S_HOME=$(pwd)
mkdir -p work
export WORK=$S2S_HOME/work
cd ../../
export TEXT2SQL_HOME=$(pwd)
cd $TEXT2SQL_HOME/tools
python2 new_format_processor.py $TEXT2SQL_HOME/data/advising.json $WORK/advising_data/

cd $S2S_HOME
python2 make_schema_loc_file.py $WORK/advising_data/query_split/ $TEXT2SQL_HOME/data/advising-schema.csv
python2 make_schema_loc_file.py $WORK/advising_data/question_split/ $TEXT2SQL_HOME/data/advising-schema.csv
cd bin/tools
python2 generate_copying_vocab.py $WORK/advising_data/query_split/
python2 generate_copying_vocab.py $WORK/advising_data/question_split/
