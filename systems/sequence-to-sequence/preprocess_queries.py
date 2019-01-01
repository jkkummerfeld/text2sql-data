import argparse
import re
import sys

#from tokenise_sql import tokenise

def preprocess(line):
    """
    Given a line of canonicalized, tokenized SQL, generate special copy-token
    versions of the field name. Tokenization is documented in
    text-to-sql-data/tools/tokenise_sql.py
    The special copy-token versions of the field names are <TABLE_NAME>,<FIELD_NAME>
    and are just so that AREA.COURSE_ID != COURSE.COURSE_ID.

    >>> preprocess('SELECT COURSE alias0 . DEPARTMENT')
    'SELECT COURSE alias0 . COURSE,DEPARTMENT'

    >>> preprocess('PROGRAM_COURSE AS PROGRAM_COURSE alias0 WHERE')
    'PROGRAM_COURSE AS PROGRAM_COURSE alias0 WHERE'

    >>> preprocess('PROGRAM_COURSE alias1 . WORKLOAD')
    'PROGRAM_COURSE alias1 . PROGRAM_COURSE,WORKLOAD'

    >>> preprocess('FROM HIGHLOW AS HIGHLOW alias0 , STATE AS STATE alias0 WHERE')
    'FROM HIGHLOW AS HIGHLOW alias0 , STATE AS STATE alias0 WHERE'
    """
    # TODO: check to make sure that the string we're substituting isn't in quotes.

    #line = tokenise(line)
    line = re.sub(r"(?P<table>\S+) alias(?P<num>\d) \. (?P<field>\S+)",
                  r"\g<table> alias\g<num> . \g<table>,\g<field>",
                  line)
    return line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modifies SQL to be a more convenient set of tokens for copying - though not executable anymore.')
    parser.add_argument('--test', help='Run a series of tests.', action='store_true')
    parser.add_argument('-i', '--input_path', help='Location of a file with one query per line to be preprocessed. Original file is not altered.')

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        sys.exit(0)

    if args.input_path:
        with open(args.input_path, 'r') as f:
            lines = [l.strip() for l in f.readlines() if len(l.strip()) > 0]
        for l in lines:
            print(preprocess(l))
