#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
from itertools import accumulate
from typing import TypedDict

DIRNAME = pathlib.Path(__file__).parent


class StatType(TypedDict):
    name: str
    regex: str


class Statistics:
    def __init__(self) -> None:
        self.stats: dict[str, StatType] = {
            "uptime": {
                "name": "Uptime",
                "regex": "Uptime\(secs\).*?(\d*\.\d*)\stotal",
            },
            "interval": {
                "name": "Interval step",
                "regex": "Uptime\(secs\).*?(\d*\.\d*)\sinterval",
            },
            "interval_stall": {
                "name": "Interval Stall",
                "regex": "Interval\sstall.*?(\d*\.\d*)\spercent",
            },
            "cumulative_stall": {
                "name": "Cumulative Stall",
                "regex": "Cumulative\sstall.*?(\d*\.\d*)\spercent",
            },
            "interval_writes": {
                "name": "Interval Writes",
                "regex": "Interval\swrites.*?(\d*\.\d*)\sMB\/s",
            },
            "cumulative_writes": {
                "name": "Cumulative Writes",
                "regex": "Cumulative\swrites.*?(\d*\.\d*)\sMB\/s",
            },
            "cumulative_compaction": {
                "name": "Cumulative Compaction",
                "regex": "Cumulative\scompaction.*?(\d*\.\d*)\sMB\/s",
            },
            "interval_compaction": {
                "name": "Interval Compaction",
                "regex": "Interval\scompaction.*?(\d*\.\d*)\sMB\/s",
            },
            "cumulative_wal": {
                "name": "Cumulative WAL",
                "regex": "Cumulative\sWAL.*?(\d*\.\d*)\swrites", 
            },
            "interval_wal": {
                "name": "Interval WAL",
                "regex": "Interval\sWAL.*?(\d*\.\d*)\swrites", 
            }, 
            "cumulative_flush": {
                "name": "Cumulative Flush",
                "regex": "Flush.*?(\d*\.\d*),", 
            }, 
            "interval_flush": {
                "name": "Interval Flush",
                "regex": "Flush.*?interval\s(\d*\.\d*)", 
            }, 
            "add_file_cumulative": {
                "name": "AddFile (GB) Cumulative",
                "regex": "AddFile\(GB\).*?\s(\d*\.\d*),", 
            }, 
            "add_file_interval": {
                "name": "AddFile (GB) Interval",
                "regex": "AddFile\(GB\).*?interval\s(\d*\.\d*)", 
            }, 
            "delays_with_ongoing_compaction": {
                "name": "cf-l0-file-count-limit-delays-with-ongoing-compaction",
                "regex": "cf-l0-file-count-limit-delays-with-ongoing-compaction.*?(\d),", 
            }, 
            "stops_with_ongoing_compaction": {
                "name": "cf-l0-file-count-limit-stops-with-ongoing-compaction",
                "regex": "cf-l0-file-count-limit-stops-with-ongoing-compaction.*?(\d),", 
            }, 
            "l0_file_count_limit_delays": {
                "name": "l0-file-count-limit-delays",
                "regex": "l0-file-count-limit-delays\:.*?(\d),", 
            }, 
            "l0_file_count_limit_stops": {
                "name": "l0-file-count-limit-stops",
                "regex": "l0-file-count-limit-stops\:.*?(\d),", 
            }, 
            "memtable_limit_delays": {
                "name": "memtable-limit-delays",
                "regex": "memtable-limit-delays\:.*?(\d),", 
            }, 
            "memtable_limit_stops": {
                "name": "memtable-limit-stops",
                "regex": "memtable-limit-stops\:.*?(\d),", 
            }, 
            "pending_compaction_bytes_delays": {
                "name": "pending-compaction-bytes-delays",
                "regex": "pending-compaction-bytes-delays\:.*?(\d),", 
            }, 
            "pending_compaction_bytes_stops": {
                "name": "pending-compaction-bytes-stops",
                "regex": "pending-compaction-bytes-stops\:.*?(\d),", 
            }, 
            "total_delays": {
                "name": "total-delays",
                "regex": "total-delays\:.*?(\d),", 
            }, 
            "total_stops": {
                "name": "total-stops",
                "regex": "total-stops\:.*?(\d),", 
            }, 
            "l0_files": {
                "name": "L0 Files",
                "regex": "L0.*?(\d)\/", 
            }, 
            "l0_size": {
                "name": "L0 Size",
                "regex": "L0.*?(\d*\.\d*)\sMB", 
            }, 
            "num_running_compactions": {
                "name": "num-running-compactions",
                "regex": "num-running-compactions.*?(\d)", 
            }, 
            "num_running_flushes": {
                "name": "num-running-flushes",
                "regex": "num-running-flushes.*?(\d)", 
            },  
            "p99.99": {
                "name": "P99.99",
                "regex": "P99\.99.*?(\d*\.\d*)", 
            },  
            "p99.9": {
                "name": "P99.9",
                "regex": "P99\.9.*?(\d*\.\d*)\sP", 
            },  
            "p99": {
                "name": "P99",
                "regex": "P99.*?(\d*\.\d*)\sP", 
            },  
            "p75": {
                "name": "P75",
                "regex": "P75.*?(\d*\.\d*)\sP", 
            },  
            "p50": {
                "name": "P50",
                "regex": "P50.*?(\d*\.\d*)\sP", 
            },  
            "L0_P99.99": {
                "name": "L0 P99.99",
                "regex": "Level\s0\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)", 
            },  
            "L1_P99.99": {
                "name": "L1 P99.99",
                "regex": "Level\s1\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)", 
            },  
            "L2_P99.99": {
                "name": "L2 P99.99",
                "regex": "Level\s2\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            }, 
            "L3_P99.99": {
                "name": "L3 P99.99",
                "regex": "Level\s3\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            }, 
            "L4_P99.99": {
                "name": "L4 P99.99",
                "regex": "Level\s4\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            }, 
            "L5_P99.99": {
                "name": "L5 P99.99",
                "regex": "Level\s5\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            }, 
            "L6_P99.99": {
                "name": "L6 P99.99",
                "regex": "Level\s6\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            }, 
            "L7_P99.99": {
                "name": "L7 P99.99",
                "regex": "Level\s7\sread\slatency.*?\s.*?\s.*?\s.*?\sP99\.99.*?(\d*\.\d*)",
            },
        }

        self.legend_list: list[str] = []
        self.plots: list[str] = []
        self.base_filename = ""

    def coordinates_filename(self) -> str:
        return self.base_filename + "_coordinates.log"

    def save_statistic(
        self, key: str, d: StatType, log: str, steps: list[float] | None = None
    ) -> None:
        matches = self.get_matches(d["regex"], log)
        new_filename = self.base_filename + f"_{key}"
        self.save_to_csv_file(matches, new_filename)

        coordinates = self.generate_coordinates(matches, steps)
        self.save_coordinates_to_file(coordinates, self.coordinates_filename())
        self.legend_list.append(d["name"])

    def clean_log(self, log: str) -> list[str]:
        regex = re.compile("(2018\S+).*\(([\d,\.]*)\).*\(([\d,\.]*)\).*\(([\d,\.]*)\)")
        path = os.path.join(os.getcwd(), "output", log)
        with open(path, "r") as f:

            matches = regex.findall(f.read())
        return [",".join(match) for match in matches]

    def get_matches(self, pattern: str, log: str) -> list[str]:
        regex = re.compile(pattern)
        path = os.path.join(os.getcwd(), log)
        with open(path, "r") as f:
            matches = regex.findall(f.read())
        return matches

    def generate_coordinates(
        self, matches: list[str], steps: list[float] | None
    ) -> list[str]:
        if not steps:
            return [f"({i*1},{match})" for i, match in enumerate(matches)]
        return [f"({key},{value})" for key, value in zip(steps, matches)]

    def save_to_csv_file(self, data: list[str], filename: str) -> None:
        os.makedirs("output", exist_ok=True)
        file_path = f"output/{filename}.csv"
        with open(file_path, "w") as f:
            f.writelines(",".join(data))
        print("Saved", filename, "to", file_path)

    def save_coordinates_to_file(
        self, data: list[str], filename: str, last: bool = False
    ) -> None:
        str_data = "".join(data)
        self.plots.append(f"\t\t\\addplot\n\tcoordinates {{ { str_data } }};\n")

    def save_coordinate_file(self, filename: str) -> None:
        os.makedirs("output", exist_ok=True)
        axis = f"""
\\begin{{tikzpicture}}
    \\begin{{axis}}[
        title={self.base_filename.replace("_", " ")},
        xlabel={{}},
        ylabel={{MB/s}},
        legend style={{
            at={{(0.5,-0.2)}},
            anchor=north,legend columns=1
        }},
        ymajorgrids=true,
        grid style=dashed,
    ]
"""
        with open(f"output/{filename}", "w") as f:
            f.write(axis)
            for plot in self.plots:
                f.write(plot)
            legend = ", ".join(self.legend_list)
            f.write(
                f"""
    \\legend{{{legend}}}
    \\end{{axis}}
\\end{{tikzpicture}}
"""
            )

    def get_steps(self, pattern: str, log: str) -> list[float]:
        interval_steps = self.get_matches(pattern, log)[::2]
        accumulated_steps = list(accumulate([float(step) for step in interval_steps]))
        rounded_steps = [round(step, 2) for step in accumulated_steps]
        return rounded_steps

    def save_all(self, log: str, statistics: set[str]) -> None:
        logfile = pathlib.Path(log)
        self.base_filename = logfile.stem
        interval_steps = self.get_steps(self.stats["interval"]["regex"], log)
        uptime_steps = [
            float(step)
            for step in self.get_matches(self.stats["uptime"]["regex"], log)[::2]
        ]
        min_interval_step = uptime_steps[0] - interval_steps[0]
        steps = [round(step - min_interval_step, 2) for step in uptime_steps]

        for key, value in self.stats.items():
            if len(statistics) > 0 and key not in statistics:
                continue
            self.save_statistic(key, value, log, steps)

        self.save_coordinate_file(self.coordinates_filename())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=str, help="logfile")
    parser.add_argument("--statistics", type=str, help="logfile")
    args = parser.parse_args()
    s = Statistics()

    statistics = (
        {arg.strip() for arg in args.statistics.split(",")}
        if args.statistics
        else set()
    )
    if len(statistics) > 0 and not statistics.intersection(s.stats.keys()):
        raise KeyError(
            f"Statistic not supported, must use one or more of \"{','.join(s.stats.keys())}\""
        )

    s.save_all(args.log, statistics)
