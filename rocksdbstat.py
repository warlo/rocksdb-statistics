#!/usr/bin/env python3
import re, argparse
import os


class Statistics:
    def __init__(self):
        self.interval_stall = {'regex': 'Interval\sstall.*?(\d*\.\d*)\spercent', 'suffix': '_interval_stall'}
        self.cumulative_stall = {'regex': 'Cumulative\sstall.*?(\d*\.\d*)\spercent', 'suffix': '_cumulative_stall'}
        self.interval_writes = {'regex': 'Interval\swrites.*?(\d*\.\d*)\sMB\/s', 'suffix': '_interval_writes'}
        self.cumulative_writes = {'regex': 'Cumulative\swrites.*?(\d*\.\d*)\sMB\/s', 'suffix': '_cumulative_writes'}

    def save_statistic(self, d, log):
        matches = self.get_matches(d['regex'], log)
        new_filename = log.split('.')[0] + f'{d["suffix"]}.csv'
        self.save_to_file(matches, new_filename)

    def save_interval_stall(self, log):
        self.save_statistic(self.interval_stall, log)

    def save_cumulative_stall(self, log):
        self.save_statistic(self.cumulative_stall, log)

    def save_interval_writes(self, log):
        self.save_statistic(self.interval_writes, log)

    def save_cumulative_writes(self, log):
        self.save_statistic(self.cumulative_writes, log)

    def clean_log(self, log):
        regex = re.compile('(2018\S+).*\(([\d,\.]*)\).*\(([\d,\.]*)\).*\(([\d,\.]*)\)')
        path = os.path.join(os.getcwd(), 'output', log)
        with open(path, 'r') as f:

            matches = regex.findall(f.read())
        return [','.join(match) for match in matches]

    def get_matches(self, regex, log):
        regex = re.compile(regex)
        path = os.path.join(os.getcwd(), log)
        with open(path, 'r') as f:
            matches = regex.findall(f.read())
        return matches

    def generate_coordinates(self, matches):
        pass

    def save_to_file(self, data, filename):
        os.makedirs('output', exist_ok=True)
        with open(f'output/{filename}', 'w') as f:
            f.writelines('\n'.join(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=str, help="logfile")
    args = parser.parse_args()
    s = Statistics()
    log = args.log
    s.save_interval_writes(log)
    s.save_cumulative_writes(log)
    s.save_interval_stall(log)
    s.save_cumulative_stall(log)
