#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags',nargs='+',required=True)
parser.add_argument('--input_folder',default='outputs')
parser.add_argument('--output_path',default='plots/alternative_reduce.png')
args = parser.parse_args()

import os
import json
import datetime
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

data = defaultdict(dict)
for filename in sorted(os.listdir(args.input_folder)):
    if not filename.endswith('.lang'):
        continue
    date_str = filename.split('geoTwitter')[1][:8]
    date = datetime.datetime.strptime(date_str, '%y-%m-%d')
    day = date.timetuple().tm_yday
    with open(os.path.join(args.input_folder,filename)) as f:
        counts = json.load(f)
    for hashtag in args.hashtags:
        data[hashtag][day] = sum(counts.get(hashtag,{}).values())



plt.figure(figsize=(12,6))
for hashtag in args.hashtags:
    days = sorted(data[hashtag])
    values = [data[hashtag][d] for d in days]
    plt.plot(days, values, label=hashtag)


plt.xlabel('Day of the year (2020)')
plt.ylabel('Number of tweets')
plt.title('Daily tweets using each hashtag in 2020')
plt.legend()
plt.tight_layout()


output_dir = os.path.dirname(args.output_path)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
plt.savefig(args.output_path)
print('saved',args.output_path)
