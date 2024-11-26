#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "XIN LI"
Semester: "Fall 2024"

The python code in this file is original work written by
"XIN LI". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os, sys

def parse_command_args() -> object:
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    filled_length = int(length * percent)
    return '#' * filled_length + ' ' * (length - filled_length) 


def get_sys_mem() -> int:
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) 
    

def get_avail_mem() -> int:
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) 

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
    else:
        ...
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
