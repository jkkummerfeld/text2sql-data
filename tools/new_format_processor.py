"""
Takes data in the new format (so far applied to GeoQuery) and
generates question_split and query_split folders as used by
seq2sql code.
Directory tree will be
dataset_name/
|
-question_split/
  |
  -train/
    |
    -train_encode.txt
    -train_decode.txt
  |
  -dev/
    |
    -dev_encode.txt
    -dev_decode.txt
  |
  -test/
    |
    -test_encode.txt
    -test_decode.txt
|
-query_split/
  |
  -train/
    |
    -train_encode.txt
    -train_decode.txt
  |
  -dev/
    |
    -dev_encode.txt
    -dev_decode.txt
  |
  -test/
    |
    -test_encode.txt
    -test_decode.txt
"""

import argparse
import os
import json

import read_new_as_old
from tokenise_sql import tokenise
from encoder_input_canonicalizer import process_sentence as preprocess_text

def build_question_split(jsons, save_loc, keep_variables=False):
    datasets = {}
    for json_dict in jsons:
        for query in [json_dict["sql"][0]]:
            sql_vars = json_dict['variables']
            for sentence in json_dict["sentences"]:
                text, variables, split = extract_sentence_fields(sentence)
                if split == "exclude":
                    continue
                if keep_variables:
                    sql = query
                    question = text
                else:
                    sql, question = read_new_as_old.insert_variables(
                        query, sql_vars, text, variables)
                sql = tokenise(sql)
                question = preprocess_text(question)
                if not split in datasets:
                    datasets[split] = []
                datasets[split].append((question, sql))
    print "Question split:"
    for k, v in sorted(datasets.items()):
        print "\t%s: %d" % (k, len(v))
    save_datasets(datasets, save_loc)

def build_nonredundant_query_split(jsons, save_loc,
                                   max_questions=None, keep_variables=False):
    import random
    datasets = {}
    for json_dict in jsons:
        split = json_dict["query-split"]
        if split == "exclude": continue
        if not split in datasets:
            datasets[split] = []
        query =json_dict["sql"][0]
        sql_vars = json_dict['variables']
        sentence = random.choice(json_dict["sentences"])
        text, variables, _ = extract_sentence_fields(sentence)
        if keep_variables:
            sql = query
            question = text
        else:
            sql, question = read_new_as_old.insert_variables(
                query, sql_vars, text, variables)
            sql = tokenise(sql)
            question = preprocess_text(question)
            datasets[split].append((question, sql))
    print "Nonredundant query split:"
    for k, v in sorted(datasets.items()):
        print "\t%s: %d" % (k, len(v))
    save_datasets(datasets, save_loc)

def build_query_split(jsons, save_loc, max_questions=None, keep_variables=False):
    datasets = {}
    for json_dict in jsons:
        split = json_dict["query-split"]
        if split == "exclude": continue
        if not split in datasets:
            datasets[split] = []
        for query in [json_dict["sql"][0]]:
            sql_vars = json_dict['variables']
            sentences = json_dict["sentences"]
            if max_questions and max_questions < len(sentences):
                sentences = sentences[:max_questions]
            for sentence in sentences:
                text, variables, _ = extract_sentence_fields(sentence)
                if keep_variables:
                    sql = query
                    question = text
                else:
                    sql, question = read_new_as_old.insert_variables(
                        query, sql_vars, text, variables)
                sql = tokenise(sql)
                question = preprocess_text(question)
                datasets[split].append((question, sql))
    print "Query split:"
    for k, v in sorted(datasets.items()):
        print "\t%s: %d" % (k, len(v))
    save_datasets(datasets, save_loc)

def extract_sentence_fields(sentence):
    text = sentence["text"]
    variables = sentence["variables"]
    split = sentence["question-split"]
    return text, variables, split

def get_jsons_from_one_file(json_loc):
    """
    Returns a list of dictionaries read in from a single
    json file, which should contain a list of dictionaries.
    """
    with open(json_loc, 'r') as f:
        list_of_dicts = json.load(f)
    return list_of_dicts

def get_jsons(json_loc):
    """
    Returns a list of dictionaries read in from the directory
    full of jsons.
    """
    fnames = [os.path.join(json_loc, name) \
              for name in os.listdir(json_loc) \
              if is_question_json(os.path.join(json_loc, name))]
    print "Read in %d jsons" % len(fnames)
    jsons = []
    for fname in fnames:
        with open(fname, 'r') as f:
            json_dict = json.load(f)
            jsons.append(json_dict)
    return jsons

def is_question_json(file_path):
    if not os.path.isfile(file_path):
        return False
    extension = os.path.splitext(file_path)[1]
    if extension.lower() != ".json":
        return False
    fname = os.path.basename(file_path)
    if not fname.startswith("question"):
        return False
    return True

def save_datasets(datasets, save_loc):
    if not os.path.exists(save_loc):
        os.makedirs(save_loc)
    for split_name, list_of_pairs in datasets.items():
        split_name = str(split_name)
        folder_name = os.path.join(save_loc, split_name)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        encode_name = os.path.join(folder_name,
                                   "%s_encode.txt" % split_name)
        decode_name = os.path.join(folder_name,
                                   "%s_decode.txt" % split_name)
        with open(encode_name, 'w') as encode_f:
            with open(decode_name, 'w') as decode_f:
                for pair in list_of_pairs:
                    encode_f.write(pair[0].encode('utf8'))
                    encode_f.write("\n")
                    decode_f.write(pair[1].encode('utf8'))
                    decode_f.write("\n")

def main(json_loc, save_loc, max_question_copies=None, keep_variables=False):
    one_file = os.path.isfile(json_loc)
    if one_file:
        jsons = get_jsons_from_one_file(json_loc)
    else:
        jsons = get_jsons(json_loc)
    # build_nonredundant_query_split(jsons, os.path.join(save_loc, "query_split"),
    #                                max_question_copies, keep_variables)
    build_query_split(jsons, os.path.join(save_loc, "query_split"),
                      max_question_copies, keep_variables)
    build_question_split(jsons, os.path.join(save_loc, "question_split"), keep_variables)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Transform the new'
    ' json-formatted data to train/ dev/ test/ encode and decode files,'
    ' or buckets for cross-validation, with encode and decode files for each bucket.')
    parser.add_argument('json_loc', help='location of json-formatted data')
    parser.add_argument('save_loc', help='location to save dataset to'
                        ' (probably somewhere in text-to-sql/data)')
    # parser.add_argument('-o', "--one_file", action='store_true',
    #                     help='All jsons are stored in one file as a list.'
    #                     ' When this flag is set, json_loc should be the json'
    #                     'file name; when this flag is off, it is the directory'
    #                     ' containing all of the jsons.')
    parser.add_argument('-m', "--max_question_copies", type=int,
                        help='Maximum number of paraphrases of a single query to '
                        'include in the dataset. Will use all paraphrases if this '
                        'is not set. ')
    parser.add_argument('-v', "--keep_variables", action='store_true',
                        help = "Keep variables (e.g., topic0) in the questions and sql.")

    args = parser.parse_args()
    main(args.json_loc, args.save_loc, args.max_question_copies, args.keep_variables)
