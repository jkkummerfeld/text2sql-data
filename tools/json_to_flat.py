#!/usr/bin/env python3

from __future__ import print_function

import json
import sys
import argparse

from tokenise_sql import tokenise

def convert_instance(data):
    var_sql = None
    var_sql = data["sql"][0]
    for sentence in data["sentences"]:
        text = sentence['text']
        sql = var_sql # Needed to do variable replacement correctly

        # Variable replacement
        if not args.keep_vars:
            for name in sentence['variables']:
                value = sentence['variables'][name]
                if len(value) == 0:
                    for variable in data['variables']:
                        if variable['name'] == name:
                            value = variable['example']
                text = value.join(text.split(name))
                if not args.keep_sql_vars:
                    sql = value.join(sql.split(name))

        # Tokenise
        if args.tokenise_sql:
            sql = tokenise(sql)

        # Select the output file
        output_file = out_train
        if args.query_split:
            if data['query-split'] == 'dev':
                output_file = out_dev
            elif data['query-split'] == 'test':
                output_file = out_test
        else:
            if sentence['question-split'] == 'dev':
                output_file = out_dev
            elif sentence['question-split'] == 'test':
                output_file = out_test
        if args.to_stdout:
            output_file = sys.stdout

        print(text, "|||", sql, file=output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads json files with data and produces information in a convenient one line per question format.')
    parser.add_argument('--keep_vars', help='Do not replace the varibales with values.', action='store_true')
    parser.add_argument('--tokenise_sql', help='Apply our tokenisation scheme to the SQL.', action='store_true')
    parser.add_argument('--query_split', help='Split based on queries, not questions.', action='store_true')
    parser.add_argument('--keep_sql_vars', help='Keep vars just in SQL.', action='store_true')
    parser.add_argument('--to_stdout', help='Print all data to stdout.', action='store_true')
    parser.add_argument('output_prefix', help='Filename prefix output_file for output files.')
    args = parser.parse_args()

    out_train = open(args.output_prefix +'.train', 'w')
    out_dev = open(args.output_prefix +'.dev', 'w')
    out_test = open(args.output_prefix +'.test', 'w')

    for line in sys.stdin:
        filenames = line.strip().split()
        for filename in filenames:
            data = json.loads(open(filename).read())
            if type(data) == list:
                for instance in data:
                    convert_instance(instance)
            else:
                convert_instance(data)

    out_train.close()
    out_dev.close()
    out_test.close()
