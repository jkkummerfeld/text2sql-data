#!/usr/bin/env python3
# Adapted by Jonathan K. Kummerfeld from https://github.com/clab/dynet/blob/master/examples/tagger/bilstmtagger.py

import argparse
from collections import Counter
import pickle
import random
import json
import sys

print("Running:\n"+ ' '.join(sys.argv))

import numpy as np

## Command line argument handling and default configuration ##

parser = argparse.ArgumentParser(description='A simple template-based text-to-SQL system.')

# IO
parser.add_argument('data', help='Data in json format', nargs='+')
parser.add_argument('--unk-max', help='Maximum count to be considered an unknown word', type=int, default=0)
parser.add_argument('--query-split', help='Use the query split rather than the question split', action='store_true')
parser.add_argument('--no-vars', help='Run without filling in variables', action='store_true')
parser.add_argument('--use-all-sql', help='Default is to use first SQL only, this makes multiple instances.', action='store_true')
parser.add_argument('--do-test-eval', help='Do the final evaluation on the test set (rather than dev).', action='store_true')
parser.add_argument('--split', help='Use this split in cross-validation.', type=int) # Used for small datasets: Academic, Restaurants, IMDB, Yelp

# Model
parser.add_argument('--mlp', help='Use a multi-layer perceptron', action='store_true')
parser.add_argument('--dim-word', help='Dimensionality of word embeddings', type=int, default=128)
parser.add_argument('--dim-hidden-lstm', help='Dimensionality of LSTM hidden vectors', type=int, default=64)
parser.add_argument('--dim-hidden-mlp', help='Dimensionality of MLP hidden vectors', type=int, default=32)
parser.add_argument('--dim-hidden-template', help='Dimensionality of MLP hidden vectors for the final template choice', type=int, default=64)
parser.add_argument('--word-vectors', help='Pre-built word embeddings')
parser.add_argument('--lstm-layers', help='Number of layers in the LSTM', type=int, default=2)

# Training
parser.add_argument('--max-iters', help='Maximum number of training iterations', type=int, default=50)
parser.add_argument('--max-bad-iters', help='Maximum number of consecutive training iterations without improvement', type=int, default=5)
parser.add_argument('--log-freq', help='Number of examples to decode between logging', type=int, default=400)
parser.add_argument('--eval-freq', help='Number of examples to decode between evaluation runs', type=int, default=800)
parser.add_argument('--train-noise', help='Noise added to word embeddings as regularization', type=float, default=0.1)
parser.add_argument('--lstm-dropout', help='Dropout for input and hidden elements of the LSTM', type=float, default=0.0)
parser.add_argument('--learning-rate', help='Learning rate for optimiser', type=float, default="0.1")

args = parser.parse_args()

import dynet as dy # Loaded late to avoid memory allocation when we just want help info

## Input ##

def insert_variables(sql, sql_variables, sent, sent_variables):
    tokens = []
    tags = []
    seen_sent_variables = set()
    for token in sent.strip().split():
        if (token not in sent_variables) or args.no_vars:
            tokens.append(token)
            tags.append("O")
        else:
            assert len(sent_variables[token]) > 0
            seen_sent_variables.add(token)
            for word in sent_variables[token].split():
                tokens.append(word)
                tags.append(token)

    sql_tokens = []
    for token in sql.strip().split():
        if token.startswith('"%') or token.startswith("'%"):
            sql_tokens.append(token[:2])
            token = token[2:]
        elif token.startswith('"') or token.startswith("'"):
            sql_tokens.append(token[0])
            token = token[1:]

        if token.endswith('%"') or token.endswith("%'"):
            sql_tokens.append(token[:-2])
            sql_tokens.append(token[-2:])
        elif token.endswith('"') or token.endswith("'"):
            sql_tokens.append(token[:-1])
            sql_tokens.append(token[-1])
        else:
            sql_tokens.append(token)

    template = []
    complete = []
    for token in sql_tokens:
        # Do the template
        if token in seen_sent_variables:
            # The token is a variable name that will be copied from the sentence
            template.append(token)
        elif (token not in sent_variables) and (token not in sql_variables):
            # The token is an SQL keyword
            template.append(token)
        elif token in sent_variables and sent_variables[token] != '':
            # The token is a variable whose value is unique to this questions,
            # but is not explicitly given
            template.append(sent_variables[token])
        else:
            # The token is a variable whose value is not unique to this
            # question and not explicitly given
            template.append(sql_variables[token])

        # Do the complete case
        if token in sent_variables and sent_variables[token] != '':
            complete.append(sent_variables[token])
        elif token in sql_variables:
            complete.append(sql_variables[token])
        else:
            complete.append(token)

    return (tokens, tags, ' '.join(template), ' '.join(complete))

def get_tagged_data_for_query(data):
    dataset = data['query-split']
    for sent_info in data['sentences']:
        if not args.query_split:
            dataset = sent_info['question-split']

        if args.split is not None:
            if str(args.split) == str(dataset):
                dataset = "test"
            else:
                dataset = "train"

        for sql in data['sql']:
            sql_vars = {}
            for sql_var in data['variables']:
                sql_vars[sql_var['name']] = sql_var['example']
            text = sent_info['text']
            text_vars = sent_info['variables']

            yield (dataset, insert_variables(sql, sql_vars, text, text_vars))

            if not args.use_all_sql:
                break

train = []
dev = []
test = []
for filename in args.data:
    with open(filename) as input_file:
        data = json.load(input_file)
        for example in data:
            for dataset, instance in get_tagged_data_for_query(example):
                if dataset == 'train':
                    train.append(instance)
                elif dataset == 'dev':
                    if args.do_test_eval:
                        train.append(instance)
                    else:
                        dev.append(instance)
                elif dataset == 'test':
                    test.append(instance)
                elif dataset == 'exclude':
                    pass
                else:
                    assert False, dataset

## Set up voacbulary ##

class Vocab:
    def __init__(self, w2i):
        self.w2i = dict(w2i)
        self.i2w = {i:w for w,i in w2i.items()}

    @classmethod
    def from_corpus(cls, corpus):
        w2i = {}
        for word in corpus:
            w2i.setdefault(word, len(w2i))
        return Vocab(w2i)

    def size(self):
        return len(self.w2i.keys())

def build_vocab(sentences):
    counts = Counter()
    words = {"<UNK>"}
    tag_set = set()
    template_set = set()
    for tokens, tags, template, complete in train:
        template_set.add(template)
        for tag in tags:
            tag_set.add(tag)
        for token in tokens:
            counts[token] += 1

    for word in counts:
        if counts[word] > args.unk_max:
            words.add(word)

    vocab_tags = Vocab.from_corpus(tag_set)
    vocab_words = Vocab.from_corpus(words)
    vocab_templates = Vocab.from_corpus(template_set)

    return vocab_words, vocab_tags, vocab_templates

vocab_words, vocab_tags, vocab_templates = build_vocab(train)
UNK = vocab_words.w2i["<UNK>"]
NWORDS = vocab_words.size()
NTAGS = vocab_tags.size()
NTEMPLATES = vocab_templates.size()

print("Running with {} templates".format(NTEMPLATES))

## Set up model ##

model = dy.Model()
trainer = dy.SimpleSGDTrainer(model, learning_rate=args.learning_rate)
DIM_WORD = args.dim_word
DIM_HIDDEN_LSTM = args.dim_hidden_lstm
DIM_HIDDEN_MLP = args.dim_hidden_mlp
DIM_HIDDEN_TEMPLATE = args.dim_hidden_template

pEmbedding = model.add_lookup_parameters((NWORDS, DIM_WORD))
if args.word_vectors is not None:
    pretrained = []
    with open(args.word_vectors,'rb') as pickleFile:
        embedding = pickle.load(pickleFile)
        for word_id in range(vocab_words.size()):
            word = vocab_words.i2w[word_id]
            if word in embedding:
                pretrained.append(embedding[word])
            else:
                pretrained.append(pEmbedding.row_as_array(word_id))
    pEmbedding.init_from_array(np.array(pretrained))
if args.mlp:
    pHidden = model.add_parameters((DIM_HIDDEN_MLP, DIM_HIDDEN_LSTM*2))
    pOutput = model.add_parameters((NTAGS, DIM_HIDDEN_MLP))
else:
    pOutput = model.add_parameters((NTAGS, DIM_HIDDEN_LSTM*2))

builders = [
    dy.LSTMBuilder(args.lstm_layers, DIM_WORD, DIM_HIDDEN_LSTM, model),
    dy.LSTMBuilder(args.lstm_layers, DIM_WORD, DIM_HIDDEN_LSTM, model),
]

pHiddenTemplate = model.add_parameters((DIM_HIDDEN_TEMPLATE, DIM_HIDDEN_LSTM*2))
pOutputTemplate = model.add_parameters((NTEMPLATES, DIM_HIDDEN_TEMPLATE))

## Training and evaluation ##

def build_tagging_graph(words, tags, template, builders, train=True):
    dy.renew_cg()

    if train and args.lstm_dropout is not None and args.lstm_dropout > 0:
        for b in builders:
            b.set_dropouts(args.lstm_dropout, args.lstm_dropout)

    f_init, b_init = [b.initial_state() for b in builders]

    wembs = [dy.lookup(pEmbedding, w) for w in words]
    if train: # Add noise in training as a regularizer
        wembs = [dy.noise(we, args.train_noise) for we in wembs]

    fw_states = [x for x in f_init.add_inputs(wembs)]
    bw_states = [x for x in b_init.add_inputs(reversed(wembs))]
    fw = [x.output() for x in fw_states]
    bw = [x.output() for x in bw_states]

    O = dy.parameter(pOutput)
    if args.mlp:
        H = dy.parameter(pHidden)
    errs = []
    pred_tags = []
    for f, b, t in zip(fw, reversed(bw), tags):
        f_b = dy.concatenate([f,b])
        if args.mlp:
            f_b = dy.tanh(H * f_b)
        r_t = O * f_b
        if train:
            err = dy.pickneglogsoftmax(r_t, t)
            errs.append(err)
        else:
            out = dy.softmax(r_t)
            chosen = np.argmax(out.npvalue())
            pred_tags.append(vocab_tags.i2w[chosen])

    O_template = dy.parameter(pOutputTemplate)
    H_template = dy.parameter(pHiddenTemplate)
    f_bt = dy.concatenate([fw_states[-1].s()[0], bw_states[-1].s()[0]])
    f_bt = dy.tanh(H_template * f_bt)
    r_tt = O_template * f_bt
    pred_template = None
    if train:
        err = dy.pickneglogsoftmax(r_tt, template)
        errs.append(err)
    else:
        out = dy.softmax(r_tt)
        chosen = np.argmax(out.npvalue())
        pred_template = vocab_templates.i2w[chosen]

    return pred_tags, pred_template, errs

def insert_tagged_tokens(tokens, tags, template):
    to_insert = {}
    cur = (None, [])
    for token, tag in zip(tokens, tags):
        if tag != cur[0]:
            if cur[0] is not None:
                value = ' '.join(cur[1])
                to_insert[cur[0]] = value
            if tag == 'O':
                cur = (None, [])
            else:
                cur = (tag, [token])
        else:
            cur[1].append(token)
    if cur[0] is not None:
        value = ' '.join(cur[1])
        to_insert[cur[0]] = value

    modified = []
    for token in template.split():
        modified.append(to_insert.get(token, token))

    return ' '.join(modified)

def run_eval(data, builders, iteration, step):
    if len(data) == 0:
        print("No data for eval")
        return -1
    correct_tags = 0.0
    total_tags = 0.0
    complete_match = 0.0
    templates_match = 0.0
    oracle = 0.0
    for tokens, tags, template, complete in data:
        word_ids = [vocab_words.w2i.get(word, UNK) for word in tokens]
        tag_ids = [0 for tag in tags]
        pred_tags, pred_template, _ = build_tagging_graph(word_ids, tag_ids, 0, builders, False)
        gold_tags = tags
        for gold, pred in zip(gold_tags, pred_tags):
            total_tags += 1
            if gold == pred: correct_tags += 1
        pred_complete = insert_tagged_tokens(tokens, pred_tags, pred_template)
        if pred_complete == complete:
            complete_match += 1
        if pred_template == template:
            templates_match += 1
        if template in vocab_templates.w2i:
            oracle += 1

    tok_acc = correct_tags / total_tags
    complete_acc = complete_match / len(data)
    template_acc = templates_match / len(data)
    oracle_acc = oracle / len(data)
    print("Eval {}-{} Tag Acc: {:>5} Template: {:>5} Complete: {:>5} Oracle: {:>5}".format(iteration, step, tok_acc, template_acc, complete_acc, oracle_acc))
    return complete_acc

tagged = 0
loss = 0
best_dev_acc = 0.0
iters_since_best_updated = 0
steps = 0
for iteration in range(args.max_iters):
    random.shuffle(train)
    for tokens, tags, template, complete in train:
        steps += 1

        # Convert to indices
        word_ids = [vocab_words.w2i.get(word, UNK) for word in tokens]
        tag_ids = [vocab_tags.w2i[tag] for tag in tags]
        template_id = vocab_templates.w2i[template]

        # Decode and update
        _, _, errs = build_tagging_graph(word_ids, tag_ids, template_id, builders)
        sum_errs = dy.esum(errs)
        loss += sum_errs.scalar_value()
        tagged += len(tag_ids)
        sum_errs.backward()
        trainer.update()

        # Log status
        if steps % args.log_freq == 0:
            trainer.status()
            print("TrainLoss {}-{}: {}".format(iteration, steps, loss / tagged))
            loss = 0
            tagged = 0
            sys.stdout.flush()
        if steps % args.eval_freq == 0:
            acc = run_eval(dev, builders, iteration, steps)
            if best_dev_acc < acc:
                best_dev_acc = acc
                iters_since_best_updated = 0
                print("New best Acc!", acc)
            sys.stdout.flush()
    iters_since_best_updated += 1
    if args.max_bad_iters > 0 and iters_since_best_updated > args.max_bad_iters:
        print("Stopping at iter {} as there have been {} iters without improvement".format(iteration, args.max_bad_iters))
        break

# Final dev
if args.do_test_eval:
    run_eval(test, builders, "End", "test")
else:
    run_eval(dev, builders, "End", "dev")
