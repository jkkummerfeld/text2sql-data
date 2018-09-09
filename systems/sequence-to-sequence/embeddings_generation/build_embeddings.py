"""
Script to generate schema embeddings from a schema csv.
The csv should include the following columns:
  - table name
  - field name (leave blank if row is for table)
  - is primary key (Y or N)
  - is foreign key (Y or N)
  - variable type

A header row is optional and can be indicated using command line
options.

The script uses pretrained word embeddings, bools, and one-hot vectors
to represent each row of the csv. It assembles these into a single
matrix representing the entire schema, which it saves as a .npy file.
"""

import argparse
import csv
import os
import re
import time

import numpy as np

from gensim.models.keyedvectors import KeyedVectors

NUM_FIELDS = 5
TYPE_CODES = {}

def get_bool(input_string):
    '''
    Returns 1 if input_string indicates yes, otherwise returns 0.
    '''
    if input_string.lower() in ['y', 'yes']:
        return np.array([1])
    return np.array([0])

def get_word_vector(input_string, model):
    '''
    Given an input string and a gensim Word2Vec model, return a vector
    representation of the string. If the string is a single word,
    simply returns the embedding for the string, or UNK embedding. If
    the string is multiple_words_with_underscores_between, tokenizes
    based on underscores and returns the means of the vectors for all
    tokens that are not UNK. Empty string returns a zero vector.
    '''
    if len(input_string) == 0:
        return np.zeros(len(model['the']))
    # Split on underscores
    words = [w.lower() for w in re.split("_", input_string) if len(w) > 0]
    vector = np.zeros(len(model['the']))
    for word in words:
        try:
            vector += model[word]
            print "added %s to vector" % word
        except:
            vector += model["unk"]
            print "%s not recognized; using unk instead." % word
    v_norm = np.linalg.norm(vector)
    if v_norm == 0:
        return vector
    return vector / v_norm


def get_type_one_hot(input_string):
    '''
    Given a string representing the type of a variable, return a
    one-hot vector representing the type. If the specified type
    is not supported, returns a one-hot representing UNK-TYPE.
    Supported types:
    - blob
    - boolean
    - char
    - clob
    - date
    - decimal
    - double precision
    - float
    - int
    - int(<11)
    - int(11)
    - int(>11)
    - numeric
    - real
    - smallint
    - varchar
    - varchar(1)
    - varchar(2-9)
    - varchar(10)
    - varchar(11-99)
    - varchar(100)
    - varchar(101-254)
    - varchar(255)
    - varchar(256+)
    - table
    - time
    - timestamp
    - UNK
    '''
    if not TYPE_CODES: # Dict is empty or contains only false-like keys.
        raise ValueError("TYPE_CODES not properly initialized.")
    if input_string[:3] == "int":
        number = get_numerical_argument(input_string)
        if not number:
            code = TYPE_CODES["int"]
        elif number < 11:
            code = TYPE_CODES["int(<11)"]
        elif number == 11:
            code = TYPE_CODES["int(11)"]
        else: # number >11
            code = TYPE_CODES["int(>11)"]
    elif input_string[:7] == "varchar":
        number = get_numerical_argument(input_string)
        if not number:
            code = TYPE_CODES["varchar"]
        elif number == 1:
            code = TYPE_CODES["varchar(1)"]
        elif 2 <= number <= 9:
            code = TYPE_CODES["varchar(2-9)"]
        elif number == 10:
            code = TYPE_CODES["varchar(10)"]
        elif 11 <= number <= 99:
            code = TYPE_CODES["varchar(11-99)"]
        elif number == 100:
            code = TYPE_CODES["varchar(100)"]
        elif 101 <= number <= 254:
            code = TYPE_CODES["varchar(101-254)"]
        elif number == 255:
            code = TYPE_CODES["varchar(255)"]
        else:
            code = TYPE_CODES["varchar(256+)"]
    else:
        pattern = "\(" #pylint: disable=anomalous-backslash-in-string
        search_string = re.split(pattern, input_string)[0]
        if search_string in TYPE_CODES:
            code = TYPE_CODES[search_string]
        else:
            code = TYPE_CODES["UNK"]
    onehot = np.zeros(len(TYPE_CODES))
    onehot[code] = 1
    return onehot

def get_numerical_argument(type_string):
    """
    Given a string of the form "text(<NUMBER>)", extracts the
    number and returns it as an int.
    """
    pattern = r"\((\d*)\)"
    match = re.search(pattern, type_string)
    if not match:
        return None
    number_string = match.group(1)
    return int(number_string)

def initialize_type_codes():
    """Initializes the numerical code for each variable type."""
    all_types = ["blob", "boolean", "char", 'clob', 'date', 'decimal',
                 'double precision', 'float', 'int', 'int(<11)', 'int(11)',
                 'int(>11)', 'numeric', 'real', 'smallint', 'varchar', 'varchar(1)',
                 'varchar(2-9)', 'varchar(10)', 'varchar(11-99)',
                 'varchar(100)', 'varchar(101-254)', 'varchar(255)',
                 'varchar(256+)', 'table', 'time', 'timestamp', 'UNK']
    for i, type_code in enumerate(all_types):
        TYPE_CODES[type_code] = i

def main(schema_path, word_embeddings_path, output_path, header=True):
    if header:
        print "Skipping header row."
    else:
        print "No header row."

    # Initialize the gensim model.
    print "Loading word vectors. This may take a moment."
    start = time.time()
    gensim_model = KeyedVectors.load_word2vec_format(
        word_embeddings_path, binary=False)
    print "Model loaded in %0.3f seconds." % (time.time() - start)
    print "Word vectors loaded."
    try:
        _ = gensim_model["unk"]
    except:
        print "unk not in model"

    # Initialize the type codes.
    initialize_type_codes()

    # We'll probably have to look up the same table names many times;
    # may as well cache them.
    cached_vectors = {}

    # Read in the schema CSV.
    all_vectors = []
    with open(schema_path, 'r') as csvfile:
        reader = csv.reader(csvfile)#, delimiter=', ')
        for row in reader:
            if header:
                header = False
                continue
            if not len(row) == NUM_FIELDS:
                print "Expected %d fields, but found %d; skipping row." % (NUM_FIELDS, len(row))
                print "\t" + ", ".join(row)
                continue
            # Get word vectors for table name and field name
            table_name = row[0].strip()
            if table_name not in cached_vectors:
                cached_vectors[table_name] = get_word_vector(
                    table_name, gensim_model)
            table_vector = cached_vectors[table_name]

            field_name = row[1].strip()
            if field_name not in cached_vectors:
                cached_vectors[field_name] = get_word_vector(
                    field_name, gensim_model)
            field_vector = cached_vectors[field_name]

            # Get bools for primary key, foreign key
            is_primary_str = row[2].strip()
            is_foreign_str = row[3].strip()
            primary_key_bool = get_bool(is_primary_str)
            foreign_key_bool = get_bool(is_foreign_str)

            # Get one-hot for type
            type_str = row[4].strip()
            #tmp
            print ", ".join([table_name, field_name,
                             str(primary_key_bool),
                             str(foreign_key_bool),
                             type_str])

            type_one_hot = get_type_one_hot(type_str)

            # Concatenate vectors
            entire_vector = np.concatenate((table_vector, field_vector,
                                            primary_key_bool,
                                            foreign_key_bool,
                                            type_one_hot))
            all_vectors.append(entire_vector)

    matrix = np.stack(all_vectors)

    # Save matrix
    np.save(output_path, matrix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate schema embeddings.")
    parser.add_argument('schema_path', help='Path to schema.csv.')
    parser.add_argument('-w', '--word_embeddings', default="data/glove.6B.50d.txt",
                        help="Absolute path to pretrained word "
                        "embeddings. Default uses GoogleNews embeddings.")
    parser.add_argument('-o', '--output_path', help="Where to save the matrix."
                        " Default is in the same directory as csv, with filename "
                        "schema_embeddings.npy")
    parser.add_argument('-n', '--no_header', action='store_true',
                        help='Indicates that the csv file has no '
                        'header, so the first row should not be '
                        'skipped.')

    args = parser.parse_args()
    print "schema path is %s" % args.schema_path
    print "word embeddings path is %s" % args.word_embeddings
    if args.output_path:
        print "output_path exists"
        output_path = args.output_path
    else:
        schema_directory = os.path.dirname(args.schema_path)
        output_path = os.path.join(schema_directory, "schema_map.npy")
        print "output_path not specified; using %s" % output_path
    main(args.schema_path, args.word_embeddings, output_path, not args.no_header)
