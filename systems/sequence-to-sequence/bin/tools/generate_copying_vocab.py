#! /usr/bin/env python

#pylint: disable=invalid-name
"""
Generate vocabularies for a set of text files. Encode vocab is
generated normally. Command line options let you generate a decode
vocabulary that assumes copying from encode, copying from schema,
both, or neither.
"""

import sys
import argparse
import collections
import logging
import os
import csv


def get_lines(fname):
  with open(fname, 'r') as f:
    lines = [l.strip() for l in f.readlines() if len(l.strip()) > 0]
  return lines

def get_schema_vocabs(schema_locs_txt):
  # Build a dict of schema vocabs
  schema_locs = get_lines(schema_locs_txt)
  unique_schema_locs = set(schema_locs)
  schema_vocabs = {}
  for loc in unique_schema_locs:
    # Get the schema from the csv file
    csv_fname = loc
    tables = []
    fields = []
    header = True
    with open(csv_fname, 'r') as f:
      reader = csv.reader(f)
      for row in reader:
        if header:
          header = False
          continue
        table_name = row[0].strip()
        field_name = row[1].strip()
        if field_name:
          fields.append(field_name)
        else:
          tables.append(table_name)
    vocab = set(tables + fields)
    # Put it in the dictionary
    schema_vocabs[loc] = vocab
    return schema_locs, schema_vocabs


parser = argparse.ArgumentParser(
    description="Generate vocabulary for a tokenized text file.")
parser.add_argument(
    "--min_frequency",
    dest="min_frequency",
    type=int,
    default=0,
    help="Minimum frequency of a word to be included in the vocabulary.")
parser.add_argument(
    "--max_vocab_size",
    dest="max_vocab_size",
    type=int,
    help="Maximum number of tokens in the vocabulary")
parser.add_argument(
    "--downcase",
    dest="downcase",
    type=bool,
    help="If set to true, downcase all text before processing.",
    default=False)
parser.add_argument(
    "infolder",
    nargs="?",
    default=sys.stdin,
    help="Folder containing train/, which should contain "
    "train_encode.txt, train_decode.txt, and train_schema_locations.txt")
parser.add_argument(
    "--delimiter",
    dest="delimiter",
    type=str,
    default=" ",
    help="Delimiter character for tokenizing. Use \" \" and \"\" for word and char level respectively."
)
args = parser.parse_args()

encode_txt = os.path.join(args.infolder,"train", "train_encode.txt")
decode_txt = os.path.join(args.infolder,"train", "train_decode.txt")
schema_locs_txt = os.path.join(args.infolder, "train", "train_schema_locations.txt")

encode_lines = get_lines(encode_txt)
decode_lines = get_lines(decode_txt)
schema_locs, schema_vocabs = get_schema_vocabs(schema_locs_txt)

# Counters for all tokens in the vocabularies
encode_cnt = collections.Counter()
decode_cnt = collections.Counter()
decode_cpy_both_cnt = collections.Counter()
decode_cpy_schema_cnt = collections.Counter()
decode_cpy_encode_cnt = collections.Counter()

for enc_line, dec_line, schema_loc in zip(encode_lines, decode_lines,
                                          schema_locs):
  enc_tokens = enc_line.split(" ")
  encode_cnt.update(enc_tokens)
  decode_tokens = dec_line.split(" ")
  decode_cnt.update(decode_tokens)
  dec_cpy_enc_tokens = [t for t in decode_tokens if t not in enc_tokens]
  decode_cpy_encode_cnt.update(dec_cpy_enc_tokens)
  schema_tokens = schema_vocabs[schema_loc]
  dec_cpy_schema_tokens = [t for t in decode_tokens if t not in schema_tokens]
  decode_cpy_schema_cnt.update(dec_cpy_schema_tokens)
  dec_cpy_both_tokens = [t for t in dec_cpy_enc_tokens if t not in
                                          schema_tokens]
  decode_cpy_both_cnt.update(dec_cpy_both_tokens)

logging.getLogger().setLevel(logging.INFO)

logging.info("Found %d unique tokens in the encode vocabulary.",
             len(encode_cnt))
logging.info("Found %d unique tokens in the decode vocabulary.",
             len(decode_cnt))
logging.info("Found %d unique tokens in the decode-copy-encoder vocabulary.",
             len(decode_cpy_encode_cnt))
logging.info("Found %d unique tokens in the decode-copy-schema vocabulary.",
             len(decode_cpy_schema_cnt))
logging.info("Found %d unique tokens in the decode-copy-both vocabulary.",
             len(decode_cpy_both_cnt))

def process_and_save(cnt, fname):
  # Filter tokens below the frequency threshold
  if args.min_frequency > 0:
    filtered_tokens = [(w, c) for w, c in cnt.most_common()
                       if c > args.min_frequency]
    cnt = collections.Counter(dict(filtered_tokens))

  logging.info("Found %d unique tokens with frequency > %d.",
               len(cnt), args.min_frequency)

  # Sort tokens by 1. frequency 2. lexically to break ties
  word_with_counts = cnt.most_common()
  word_with_counts = sorted(
      word_with_counts, key=lambda x: (x[1], x[0]), reverse=True)

  # Take only max-vocab
  if args.max_vocab_size is not None:
    word_with_counts = word_with_counts[:args.max_vocab_size]

  with open(os.path.join(args.infolder, fname), "w") as f:
    for word, count in word_with_counts:
      f.write("{}\t{}".format(word, count))
      f.write("\n")

process_and_save(encode_cnt, "encode_vocab.txt")
process_and_save(decode_cnt, "decode_vocab.txt")
process_and_save(decode_cpy_encode_cnt, "decode_copy_encode_vocab.txt")
process_and_save(decode_cpy_schema_cnt, "decode_copy_schema_vocab.txt")
process_and_save(decode_cpy_both_cnt, "decode_copy_both_vocab.txt")
