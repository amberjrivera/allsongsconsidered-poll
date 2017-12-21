#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import argparse


def run(top100, pivot):

    top100 = pd.read_csv(top100)
    pivot = pd.read_csv(pivot)

    # merge with original data to bring album and artist
    merged = top100.merge(pivot, on='Cluster ID', how='left')
    # Drop duplicates by Cluster ID
    clean = merged[['Cluster ID','album', 'artist',
                    '4', '5', '6', '7', '8', '9', '10', '11',
                    'agg_ranking', 'rank']]
    clean.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'paths', metavar='PATHS', nargs='+', help='')
    args = parser.parse_args()
    run(args.paths[0], args.paths[1])