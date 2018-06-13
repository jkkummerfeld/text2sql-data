#!/usr/bin/env python3

from __future__ import print_function

import json
import argparse
import re
import sys

def update_quotes(token, in_squote, in_dquote):
    for char in token:
        if char == "'" and (not in_dquote):
            in_squote = not in_squote
        elif char == '"' and (not in_squote):
            in_dquote = not in_dquote
    return in_squote, in_dquote

def tokenise(query):
    """Adjust a query to have quotes and braces as tokens.

    >>> tokenise('test "%test%" test')
    'test "% test %" test'
    >>> tokenise("test '%test%' test")
    "test '% test %' test"
    >>> tokenise('test "test" test')
    'test " test " test'
    >>> tokenise("test 'test' test")
    "test ' test ' test"
    >>> tokenise("min( test )")
    'min ( test )'
    >>> tokenise("test test.test")
    'test test . test'
    >>> tokenise("test testalias0.test")
    'test test alias0 . test'
    >>> tokenise("test TESTalias0")
    'test TEST alias0'
    """
    tokens = []
    in_squote, in_dquote = False, False
    for token in query.split():
        # Handle prefixes
        if not (in_squote or in_dquote):
            if token.startswith("'%") or token.startswith('"%'):
                if token[0] == "'": in_squote = True
                else: in_dquote = True
                tokens.append(token[:2])
                token = token[2:]
            elif token.startswith("'") or token.startswith('"'):
                if token[0] == "'": in_squote = True
                else: in_dquote = True
                tokens.append(token[0])
                token = token[1:]

        # Handle mid-token aliases
        if not (in_squote or in_dquote):
            parts = token.split(".")
            if len(parts) == 2:
                table = parts[0]
                field = parts[1]
                if 'alias' in table:
                    table_parts = table.split('alias')
                    tokens.append('alias'.join(table_parts[:-1]))
                    tokens.append('alias'+ table_parts[-1])
                else:
                    tokens.append(table)
                tokens.append('.')
                token = field

        # Handle aliases without field name.
        if not (in_squote or in_dquote):
            m = re.search(r"(?P<table>[A-Z_]+)(?P<alias>alias\d+)", token)
            if m:
                tokens.append(m.group("table"))
                tokens.append(m.group("alias"))
                continue

        # Handle suffixes
        if (in_squote and token.endswith("%'")) or \
                (in_dquote and token.endswith('%"')):
            tokens.append(token[:-2])
            tokens.append(token[-2:])
        elif (in_squote and token.endswith("'")) or \
                (in_dquote and token.endswith('"')):
            tokens.append(token[:-1])
            tokens.append(token[-1])
        elif (not (in_squote or in_dquote)) and len(token) > 1 and token.endswith("("):
            tokens.append(token[:-1])
            tokens.append(token[-1])
        else:
            tokens.append(token)
        in_squote, in_dquote = update_quotes(token, in_squote, in_dquote)

    return ' '.join(tokens)

function_words = {
    "count", "lower", "max", "min", "sum", "COUNT", "LOWER", "MAX", "MIN",
    "SUM",
}
def untokenise(query):
    """Adjust a query to return to normal executable form.

    >>> untokenise('test " test " test')
    'test "test" test'
    >>> untokenise("test ' test ' test")
    "test 'test' test"
    >>> untokenise('test "% test %" test')
    'test "%test%" test'
    >>> untokenise("test '% test %' test")
    "test '%test%' test"
    >>> untokenise("min ( test )")
    'min( test )'
    >>> untokenise("test test . test")
    'test test.test'
    >>> untokenise("test test alias0 . test")
    'test testalias0.test'
    >>> untokenise("test TEST alias0 test")
    'test TESTalias0 test'
    """
    tokens = []
    in_squote, in_dquote = False, False
    for token in query.split():
        if in_squote and (token in ["%'", "'"] or tokens[-1] in ["'%", "'"]):
            tokens[-1] += token
        elif in_dquote and (token in ['%"', '"'] or tokens[-1] in ['"%', '"']):
            tokens[-1] += token
        elif not (in_squote or in_dquote) and token == "(" and tokens[-1] in function_words:
            tokens[-1] += token
        elif (not (in_squote or in_dquote)) and (token.startswith("alias") or token == '.'):
            tokens[-1] += token
        elif (not (in_squote or in_dquote)) and (len(tokens) > 0 and tokens[-1].endswith(".")):
            tokens[-1] += token
        else:
            tokens.append(token)
        in_squote, in_dquote = update_quotes(token, in_squote, in_dquote)

    return ' '.join(tokens)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modifies SQL to be a more convenient set of tokens - though not executable anymore.')
    parser.add_argument('--tokenise', help='Convert to tokens.', action='store_true')
    parser.add_argument('--untokenise', help='Return to normal.', action='store_true')
    parser.add_argument('--test', help='Run a series of tests.', action='store_true')
    args = parser.parse_args()

    # Test
    if args.test:
        import doctest
        doctest.testmod()
        sys.exit(0)

    # Read
    data = json.load(sys.stdin)

    # Process
    nqueries = []
    for query in data['sql']:
        if args.tokenise:
            nqueries.append(tokenise(query))
        elif args.untokenise:
            nqueries.append(untokenise(query))
        else:
            nqueries.append(query)
    data['sql'] = nqueries

    # Output
    print(json.dumps(data, indent=4, sort_keys=True))
