#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import csv
import sys
import os
import arrow
import collections

# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../data')
INPUT_FILE = '2017_responses'
OUTPUT_PATH = os.path.join(cwd, '../output')

DUPE_DICT_KEYS = ['Album Title #1', 'Album Title #2', 'Album Title #3',
                  'Album Title #4', 'Album Title #5',
                  'Artist #1', 'Artist #2', 'Artist #3',
                  'Artist #4', 'Artist #5']


def find_dupe(row1, row2):
    """
    Check if pair of rows are identical in a given set of columns
    """

    # Do all row values match? If not, not a dupe
    for key in DUPE_DICT_KEYS:
        if row1[key].strip() != row2[key].strip():
            return False
    return True


def mark_ballot_stuffing_delta(row, i, rows,
                               duplicate_threshold,
                               random_order_threshold):
    """
    Modifies the list elements in place adding a smelly attribute to each row
    dictionary that is equal to the searched row within a timedelta
    Added random ordering detection within a different smaller time delta
    """
    timestamp = arrow.get(row['Timestamp'], 'M/D/YYYY H:m:s')
    row_data = [v.lower().strip() for k, v in row.iteritems() if k in DUPE_DICT_KEYS]

    while i < (len(rows) - 1):
        i += 1
        next_row = rows[i]
        next_row_data = [v.lower().strip() for k, v in next_row.iteritems() if k in DUPE_DICT_KEYS]
        next_timestamp = arrow.get(next_row['Timestamp'], 'M/D/YYYY H:m:s')
        timedelta = next_timestamp - timestamp
        if timedelta.total_seconds() < duplicate_threshold:
            if find_dupe(row, next_row):
                next_row['smelly'] = True
            if timedelta.total_seconds() < random_order_threshold:
                if collections.Counter(row_data) == collections.Counter(next_row_data):
                    next_row['smelly'] = True
        else:
            break


def run(args):
    """
    Parse allsongsconsidered form results and remove duplicate entries
    within a time window passed as a parameter
    """
    rows = []
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    rows = list(reader)
    rows = rows[1:]
    for idx, row in enumerate(rows):
        # First of all mark next rows that are identical within time window
        mark_ballot_stuffing_delta(row, idx, rows,
                                   args.duplicate_threshold,
                                   args.random_order_threshold)
        # if this row has been marked as smelly ignore
        # in output otherwise write to output file
        try:
            row['smelly']
        except KeyError:
            writer.writerow(row)


if __name__ == '__main__':
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description="Clean Ballot Stuffing")
    parser.add_argument('--duplicate_threshold',
                        type=int,
                        help="duplicate threshold (sec)",
                        required=True)
    parser.add_argument('--random_order_threshold',
                        type=int,
                        help="random order duplicate threshold (sec)",
                        required=True)
    args = parser.parse_args()
    run(args)

