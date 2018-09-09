#!/usr/bin/env python3

# Example:
# New:
#  {
#      "sentences": [
#          {
#              "data-split": "train",
#              "text": "what is the capital of states that have cities named var0",
#              "variables": {
#                  "var0": "durham"
#              }
#          }
#      ],
#      "sql": [
#          "SELECT STATE.CAPITAL FROM CITY , STATE WHERE CITY.CITY_NAME = var0 AND STATE.STATE_NAME = CITY.STATE_NAME ;"
#      ],
#      "variables": [
#          {
#              "example": "durham",
#              "location": "both",
#              "name": "var0",
#              "type": "city"
#          }
#      ]
#  }
#
# Old:
#  {
#      "paraphrases": [],
#      "sentence": "what is the capital of states that have cities named durham",
#      "sentence-with-vars": "",
#      "sql": [
#          "SELECT STATE.CAPITAL FROM CITY , STATE WHERE CITY.CITY_NAME = \"durham\" AND STATE.STATE_NAME = CITY.STATE_NAME ;"
#      ],
#      "sql-with-vars": "",
#      "variables": []
#  } 

import json
import sys

def insert_variables(sql, sql_variables, sent, sent_variables):
    for info in sql_variables:
        name = info['name']
        value = info['example']
        if name in sent_variables and sent_variables[name] != "":
            value = sent_variables[name]
        sent = value.join(sent.split(name))
        qvalue = '{}'.format(value)
        sql = qvalue.join(sql.split(name))
    return (sql, sent)

def convert(new_data):
    for sent_pos in range(len(new_data['sentences'])):
        for sql_pos in range(len(new_data['sql'])):
            sql = new_data['sql'][sql_pos]
            sql_vars = new_data['variables']
            sentence = new_data['sentences'][sent_pos]['text']
            variables = new_data['sentences'][sent_pos]['variables']

            old_data = {
                "paraphrases": [],
                "sentence": "",
                "sentence-with-vars": "",
                "sql": [],
                "sql-with-vars": "",
                "variables": []
            }

            sql, sentence = insert_variables(sql, sql_vars, sentence, variables)

            old_data['sentence'] = sentence
            old_data['sql'].append(sql)

            yield old_data

if __name__ == '__main__':
    for line in sys.stdin:
        in_file = open(line.strip())
        new_data = json.load(in_file)
        in_file.close()

        for old_data in convert(new_data):
            print(json.dumps(old_data, indent=4, sort_keys=True))

