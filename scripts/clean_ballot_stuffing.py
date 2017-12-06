#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import arrow

DUPLICATE_TIME_THRESHOLD = 60 * 60

def find_dupe(row, previousrow):
    """
        Check if pair of rows are identical
    """

    row['Timestamp'] = ''
    previousrow['Timestamp'] = ''

    for col in row:
        if row[col] != previousrow[col]:
            return False

    return True

def find_oddities(row, idx, album_list):
    """
        Search backwards to see if current row if a dupe of something that came before
    """
    row['smelly'] = False

    # Check for dupes in previous time window
    previousrow = album_list[idx]
    delta = row['Timestamp'] - previousrow['Timestamp']

    # while difference in seconds is less than 3600
    # while delta.seconds < DUPLICATE_TIME_THRESHOLD and delta.seconds > 0:
        # row['smelly'] = find_dupe(row, previousrow)
        # print(idx)
        # idx = idx - 1
        # previousrow = album_list[idx]
        # delta = row['Timestamp'] - previousrow['Timestamp']

def process():
    # import data
    albums = pd.read_csv("../data/2017_responses.csv")

    # Turn dataframe into list for easier handling of oddity detection?
    album_list = albums.to_dict('records')

    # format arrow with timestamp
    for row in album_list:
        row['Timestamp'] = arrow.get(row["Timestamp"], 'M/D/YYYY H:m:s')

    # handle oddity detection
    for idx, row in enumerate(album_list):
        find_oddities(row, idx - 1, album_list)

    # Cast back to dataframe
    albums = pd.DataFrame(album_list)

    # Weed out rows with smells
    export = albums[albums['smelly'] == False]
    export.to_csv('../output/2017_responses_clean.csv')

if __name__ == '__main__':
    process()