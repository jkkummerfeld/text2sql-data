"""
A script to build a schema map matrix from a schema map csv. The csv
should contain the following four columns:
  - From table name
  - From column name
  - To table name
  - To column name

The resulting matrix will use pretrained embeddings to represent each
table name and column name. It will build a single row vector for each
row of the csv, then stack them into a matrix, which is saved as a
.npy.
"""
import argparse
import csv
import os
import re
import time

import numpy as np

from gensim.models.keyedvectors import KeyedVectors


NUM_FIELDS = 4

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

def main(schema_path, word_embeddings_path, output_path,
         header=True, zero_vector=False):
    """The logic of the script."""
    if header:
        print "Skipping header row."
    else:
        print "No header row."

    # Initialize the gensim model.
    print "Loading word vectors. This may take a moment."
    start = time.time()
    gensim_model = KeyedVectors.load_word2vec_format(word_embeddings_path, binary=False)
    print "Model loaded in %0.3f seconds." % (time.time() - start)
    print "Word vectors loaded."
    try:
        _ = gensim_model["unk"]
    except:
        print "unk not in model"

    # We'll probably have to look up the same table and field names many times;
    # may as well cache them.
    cached_vectors = {}

    # Read in the schema CSV.
    all_vectors = []
    with open(schema_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if header:
                header = False
                continue
            if not len(row) == NUM_FIELDS:
                print "Expected %d fields, but found %d; skipping row." % (NUM_FIELDS, len(row))
                print "\t" + ", ".join(row)
                continue
            # Get word vectors for table names and field names
            from_table_name = row[0].strip()
            from_field_name = row[1].strip()
            to_table_name = row[2].strip()
            to_field_name = row[3].strip()
            vectors = []
            for name in [from_table_name, to_table_name,
                         from_field_name, to_field_name]:
                if name not in cached_vectors:
                    cached_vectors[name] = get_word_vector(name, gensim_model)
                current_vector = cached_vectors[name]
                vectors.append(current_vector)

            # Concatenate the four vectors
            entire_vector = np.concatenate(vectors)
            all_vectors.append(entire_vector)
    if zero_vector:
        print "Appending zero vector"
        zeros = np.zeros_like(all_vectors[0])
        all_vectors.append(zeros)

    matrix = np.stack(all_vectors)

    print "schema_map shape: %s" % str(matrix.shape)

    # Save matrix
    np.save(output_path, matrix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate schema_map.npy.")
    parser.add_argument('schema_path', help='Path to schema_map.csv.')
    parser.add_argument('-w', '--word_embeddings', default="data/glove.6B.50d.txt",
                        help="Absolute path to pretrained word embeddings. "
                        "Default uses GoogleNews embeddings.")
    parser.add_argument('-o', '--output_path', help="Where to save the matrix."
                        " Default is in the same directory as csv, with filename "
                        "schema_map.npy")
    parser.add_argument('-n', '--no_header', action='store_true',
                        help="Indicates that the csv file has no header, "
                        "so the first row should not be skipped.")
    parser.add_argument('-z', '--zero_vector', action='store_true',
                        help="Add a vector of zeros to the end of the matrix. "
                        "This gives the model the option of not paying attention "
                        "to the map at a particular timestep.")

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
    main(args.schema_path, args.word_embeddings, output_path, not args.no_header,
         args.zero_vector)
