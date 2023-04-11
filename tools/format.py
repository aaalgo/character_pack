#!/usr/bin/env python3
import os
import yaml
import pickle
from collections import defaultdict

def load (path):
    with open(path, 'rb') as f:
        dump = pickle.load(f)
    params = dump['params']
    trace = dump['trace']
    resp = defaultdict(lambda : [])
    for msg in trace:
        key = msg.get('save_to', None)
        if key is None:
            continue
        msg = msg['result']['choices'][0]['message']
        resp[key].append(msg['content'])
    resp.update(params)
    return resp

def join (lines):
    ll = []
    for line in lines:
        #print(line)
        #print('---')
        for x in line.split('\n'):
            ll.append(x.strip())
    return ' '.join(ll)

def extract_dialog (resp, char_name, user_name = 'PersonA'):
    txt = ' '.join(resp)
    txt = txt.replace('%s:' % char_name, '{{char}}')
    txt = txt.replace('%s:' % user_name, '{{user}}')
    cur = txt.find('{{')
    txt = txt[cur:]
    lines = []
    while True:
        nxt = txt.find('{{', 2)
        if not nxt is None:
            one = txt[:nxt].strip()
        else:
            one = txt.strip()
        if len(one)> 10:
            lines.append(one)
        if nxt < 0:
            break
        txt = txt[nxt:]
    return lines

def generate (path, resp):
    name = resp['name']
    out = {}
    out['name'] = name
    out['context'] = join(resp['context'])
    out['greeting'] = '%s is talking to you.' % name
    out['example_dialog'] = extract_dialog(resp['example_dialog'], name)
    with open(path, 'w') as f:
        f.write('name: "%s"\n' % out['name'])
        f.write('context: |-\n  ')
        f.write(out['context'])
        f.write('\n')
        f.write('greeting: |-\n  ')
        f.write(out['greeting'])
        f.write('\n')
        f.write('example_dialogue: |-\n')
        for line in out['example_dialog']:
            f.write('  %s\n' % line)

if __name__ == '__main__':
    generate('Trump.yml', load('Trump.pkl'))
