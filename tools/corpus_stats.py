#!/usr/bin/env python3

from __future__ import print_function

import argparse
import json
import sys

from collections import Counter

def update_in_quote(in_quote, token):
    if '"' in token and len(token.split('"')) % 2 == 0:
        in_quote[0] = not in_quote[0]
    if "'" in token and len(token.split("'")) % 2 == 0:
        in_quote[1] = not in_quote[1]

def process_query(data, stats):
    stats['sentences'] += len(data['sentences'])
    stats['queries'] += 1

    # Calculate number of SELECTS
    for sql in data['sql']:
        selects = 0
        in_quote = [False, False]
        for token in sql.split():
            if token == 'SELECT' and (not (in_quote[0] or in_quote[1])):
                selects += 1
            update_in_quote(in_quote, token)
            
        stats["SQL-selects-{}".format(selects)] += 1

    # Calculate depth and breadth
    for sql in data['sql']:
        max_depth = 0
        max_breadth = 1
        depth = 0
        prev = None
        other_bracket = []
        breadth = [0]
        in_quote = [False, False]
        for token in sql.split():
            if in_quote[0] or in_quote[1]:
                update_in_quote(in_quote, token)
            elif token == 'SELECT':
                depth += 1
                max_depth = max(max_depth, depth)
                other_bracket.append(0)
                breadth[-1] += 1
                breadth.append(0)
            elif '(' in prev:
                other_bracket[-1] += 1
                update_in_quote(in_quote, token)
            elif token == ')':
                if other_bracket[-1] == 0:
                    depth -= 1
                    other_bracket.pop()
                    possible = breadth.pop()
                    max_breadth = max(max_breadth, possible)
                else:
                    other_bracket[-1] -= 1
            else:
                update_in_quote(in_quote, token)
            
            if '(' in token and ')' in token:
                prev = "SQL_FUNCTION"
            else:
                prev = token
        assert len(other_bracket) == 1 and other_bracket[0] == 0, sql
        assert depth == 1, sql
        stats["SQL-depth-{}".format(max_depth)] += 1
        stats["SQL-breadth-{}".format(max_breadth)] += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prints stats about the specified files.')
    parser.add_argument('--per-file-stats', help='Show stats on each file as well as overall', action='store_true')
    parser.add_argument('json_files', help='File in our json format', nargs='+')
    args = parser.parse_args()

    total_stats = Counter()
    for filename in args.json_files:
        cur_stats = Counter()
        data = json.load(open(filename))
        if type(data) == list:
            for query in data:
                if args.per_file_stats:
                    process_query(query, cur_stats)
                process_query(query, total_stats)
        else:
            if args.per_file_stats:
                process_query(data, cur_stats)
            process_query(data, total_stats)

        if args.per_file_stats:
            for stat in cur_stats:
                print(filename, stat, cur_stats[stat])

    start = ''
    if args.per_file_stats:
        start = "Overall: "
    for stat in total_stats:
        print(start + stat, total_stats[stat])

