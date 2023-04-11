#!/usr/bin/env python3
import os
import yaml
import pickle
import pandas as pd
import openai

#openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

#assert len(openai.organization) > 0
assert len(openai.api_key) > 0

TEMPLATE = [
    {'role': 'system', 'content': 'The AI assistant is to answer the user\'s question in a concise style.'},
    {'role': 'user', 'content': 'Who is {full_name}? Please describe in one sentence.'},
    {'save_to': 'context'},
    {'role': 'user', 'content': 'Please briefly describes the personality of {name}, within 100 words.'},
    {'save_to': 'context'},
    {'role': 'user', 'content': 'PersonA is one of {name}\'s friends. Please generate a typical conversation between PersonA and {name} of {count} dialogs.'},
    {'save_to': 'example_dialog'}
]

def query_chatgpt (params, save_to):
    trace = []
    messages = []
    for tmpl in TEMPLATE:
        if 'save_to' in tmpl:
            result = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages)
            one = result['choices'][0]['message']
            messages.append({'role': one['role'], 'content': one['content']})
            trace.append({
                'save_to': tmpl['save_to'],
                'result': result
                })
        else:
            one = {
                'role': tmpl['role'],
                'content': tmpl['content'].format(**params)
                }
            trace.append(one)
            messages.append(one)
    with open(save_to, 'wb') as f:
        pickle.dump({'params': params,
                     'trace': trace},
                     f)

class Character:
    def __init__ (self, name, cache=True):
        pass


if __name__ == '__main__':
    df = pd.read_csv('../data/names.csv')
    for _, row in df.iterrows():
        sample = dict(row)
        sample['count'] = 10
        cache = '%s.pkl' % sample['name']
        if not os.path.exists(cache):
            print("Querying %s..." % sample['full_name'])
            query_chatgpt(sample, cache)
