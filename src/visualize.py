#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output_folder',default='plots')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)

items = items[:10]
items = items[::-1]

for k,v in items:
    print(k,':',v)

keys = [k for k,v in items]
values = [v for k,v in items]

if args.input_path.endswith('.country'):
    xlabel = 'Country'
else:
    xlabel = 'Language'

plt.figure(figsize=(10,6))
plt.bar(keys, values)
plt.xlabel(xlabel)
if args.percent:
    plt.ylabel('Fraction of tweets')
else:
    plt.ylabel('Number of tweets')
plt.title('Top 10 by ' + xlabel.lower())
plt.tight_layout()

os.makedirs(args.output_folder, exist_ok=True)
output_name = os.path.basename(args.input_path) + '_' + args.key.lstrip('#')
if args.percent:
    output_name += '_percent'
output_path = os.path.join(args.output_folder, output_name + '.png')
plt.savefig(output_path)
print('saved',output_path)
