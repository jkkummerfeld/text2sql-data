import argparse


def get_lines(fname):
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines() if len(l.strip()) > 0]
    while lines[0].lower().startswith("loading"):
        lines = lines[1:]
    return lines

def single_set_analysis(question_loc, gold_loc, system_output, starting_line=0):
    correct = 0
    count = 0
    right = []
    wrong = []
    questions = get_lines(question_loc)
    gold_queries = get_lines(gold_loc)
    system_queries = system_output[starting_line:]
    for question, gold, system in zip(questions, gold_queries, system_queries):
        count += 1
        if gold == system:
            correct += 1
            right.append((question, gold, system))
        else:
            wrong.append((question, gold, system))
    accuracy = 0.
    if count > 0:
        accuracy = float(correct) / count
    system_bookmark = starting_line + count
    return (correct, count, right, wrong, accuracy, system_bookmark)

def print_results(results, total_correct, total_count, right, wrong):
    for gold_loc, acc in results.items():
        print "Accuracy on %s is %.4f" % (gold_loc, acc)
    if total_count > 0:
        print "Overall accuracy is %.4f" % (float(total_correct)/total_count)
    else:
        print "Overall accuracy is undefined."

    print
    print "="*10 + "WRONG" + "="*10

    for triple in wrong:
        print "Q:", triple[0]
        print "Gold:", triple[1]
        print "System:", triple[2]
        print

    print
    print "="*10 + "RIGHT" + "="*10
    print

    for tup in right:
        print "Q:", tup[0]
        print "query:", tup[1]
        print


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='display comparison with gold and accuracy')
    parser.add_argument('-q', '--question_loc', nargs='+',
                        help='locations of questions (probably $DEV_SOURCES')
    parser.add_argument('-g', '--gold_loc',  nargs='+',
                        help='locations of gold (probably $DEV_TARGETS')
    parser.add_argument('-s', '--system_loc',
                        help='location of system outputs'
                        '(probably $MODEL_DIR/output.txt')

    args = parser.parse_args()
    question_locs = args.question_loc
    gold_locs = args.gold_loc
    system_output = get_lines(args.system_loc)
    system_bookmark = 0
    results = {}
    total_count = 0
    total_correct = 0
    all_right = []
    all_wrong = []
    for question_loc, gold_loc in zip(question_locs, gold_locs):
        (correct, count, right, wrong, accuracy,
         system_bookmark) = single_set_analysis(question_loc, gold_loc,
                                                system_output, system_bookmark)
        total_correct += correct
        total_count += count
        all_right.extend(right)
        all_wrong.extend(wrong)
        results[gold_loc] = accuracy
    if system_bookmark < len(system_output):
        print "System bookmark ended at %d, but system output length was %d" %(
            system_bookmark, len(system_output))
    print_results(results, total_correct, total_count, all_right, all_wrong)
