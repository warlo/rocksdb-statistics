#!/usr/bin/env python3
import re, argparse
import os


class Statistics:
    def __init__(self):
        self.stall = 'Cumulative\sstall.*?(\d*\.\d*)\spercent'
        self.interval_writes = 'Interval\swrites.*?(\d*\.\d*)\sMB\/s'

    def save_stall(self, log):
        matches = self.get_matches(self.stall, log)
        new_filename = log.split('.')[0] + '_stall.csv'
        self.save_to_file(matches, new_filename)

    def save_interval_writes(self, log):
        matches = self.get_matches(self.interval_writes, log)
        new_filename = log.split('.')[0] + '_interval.csv'
        self.save_to_file(matches, new_filename)

    def clean_log(self, log):
        regex = re.compile('(2018\S+).*\(([\d,\.]*)\).*\(([\d,\.]*)\).*\(([\d,\.]*)\)')
        path = os.path.join(os.getcwd(), log)
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
        with open(filename, 'w') as f:
            f.writelines('\n'.join(data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=str, help="logfile")
    args = parser.parse_args()
    s = Statistics()
    log = args.log
    s.save_interval_writes(log)
    s.save_stall(log)
