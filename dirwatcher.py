#!/usr/bin/env python3

import signal
import logging
import time
import sys
import argparse
import os
# globals
exit_flag = False
# create logger
formatter = logging.Formatter(
    "%(asctime)s: %(name)s: %(levelname)s: [%(threadName)s]: %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("dirwatcher.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

watch_dict = {}


def scan_single_file(fullpath, magic_text):
    """scans a file for the magic text"""
    only_file = fullpath.split("/")[-1]
    with open(fullpath, "r") as f:
        line = f.readline()
        cnt = 1
        while line:
            if magic_text in line:
                logger.info(f"{magic_text} found on line {cnt} of {only_file}")
            line = f.readline()
            cnt += 1


def detect_added_files(name):
    """logs if a file has been added to the directory"""
    only_file = name.split("/")[-1]
    if name not in watch_dict:
        logger.info(f"file created: {only_file}")
        watch_dict.update({name: None})


def detect_removed_files(files):
    """logs if a file has been removed from the directory"""
    if sorted(files) == sorted(watch_dict.keys()):
        pass
    else:
        deleted = set(watch_dict.keys()) - set(files)
        to_str = "".join(list(deleted))
        logger.info(f"file removed: {to_str}")
        watch_dict.pop(to_str)


def watch_dir(text, dir, EXT):
    """watching the directory for any and all changes"""
    files_list = []
    if os.path.isdir(dir):
        for root, _, files in os.walk(dir, topdown=False):
            for name in files:
                fullpath = os.path.join(root, name)
                if name.endswith(EXT):
                    if detect_added_files(fullpath):
                        break
                    if scan_single_file(fullpath, text):
                        break
                    files_list.append(fullpath)
            if detect_removed_files(files_list):
                break
                print(os.path.join(root, name))
    else:
        logger.error(f"{dir} does not exist")


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """

    # log the associated signal name (the python3 way)
    logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", type=int,
                        help="controls the polling interval")
    parser.add_argument("-e", "--ext",
                        help="filters what kind of file extension to look for")
    parser.add_argument("magic",
                        help="specifics the magic text to search for")
    parser.add_argument("path",
                        help="specify the directory to watch")
    return parser


def main(args):
    # Hook these two signals from the OS .. 
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    magic = ns.magic
    EXT = ns.ext
    path = ns.path
    polling_interval = ns.interval
    print(magic)
    print(EXT)
    print(path)
    print(polling_interval)

    while not exit_flag:
        try:
            watch_dir(magic, path, EXT)
            # call my directory watching function..
        except Exception as e:
            logger.exception(e)
            # This is an UNHANDLED exception
            # Log an ERROR level message here

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start.


if __name__ == '__main__':
    main(sys.argv[1:])
