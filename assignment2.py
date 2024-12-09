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
    parser.add_argument("-H", "--huamn-readable", action = "store_true", help="Display memory values in human readable format.")
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
    try:
        result = os.popen(f'pidof{app_name}').read()
        if result:
            return result.split()
        else:
            return [] 
    except (FileNotFoundError, NotADirectoryError):
        print (f'{app_name} not found')
        return [] 


def rss_mem_of_pid(proc_id: str) -> int:
    try:
        smaps_path = f'/proc/{proc_id}/smaps'
        with open(smaps_path, 'r') as f:
            for line in f:
                if line.startswith("VmRss:"):
                    rss_total = int(line.split()[1])
                    return rss_total
        return 0
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        print (f'{proc_id} not found')
        return 0 


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
        total_mem = get_sys_mem()
        avail_mem = get_avail_mem()
        used_mem = total_mem - avail_mem

        print(f"Used Memory: {bytes_to_human_r(used_mem) if args.human_readable else f'{used_mem} KiB'}"
              f"{percent_to_graph(used_mem / total_mem, args.length)}")
        print(f"Total Memory: {bytes_to_human_r(total_mem) if args.human_readable else f'{total_mem} KiB'}")
    else:
        pids = pids_of_prog(args.program)
        if not pids:
            print(f"No processes found for program: {args.program}")
        else:
            total_used = 0
            for pid in pids:
                rss = rss_mem_of_pid(pid)
                total_used += rss
                print(f"pid {bytes_to_human_r(rss) if args.human_readable else f'{rss} KiB'}"
                      f"{percent_to_graph(rss / get_sys_mem(), args.length)}")
            print(f"Total Used: {bytes_to_human_r(total_used) if args.human_readable else f'{total_used} KiB'}")
