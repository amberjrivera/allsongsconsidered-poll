#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../output')
INPUT_FILE = '2017_responses_deduped'
OUTPUT_PATH = os.path.join(cwd, '../output')


def rankEm():
    data = pd.read_csv("%s/%s.csv" % (INPUT_PATH, INPUT_FILE))
    # Calculate sum of points by day and dedupe cluster
    grouped = data.groupby(['day', 'Cluster ID'], as_index=False)['points'].sum()
    # Add a rank column per day in descending order as an integer
    grouped['rank'] = grouped.groupby(["day"])["points"].rank(
        method='dense', ascending=False).astype(int)

    #create pivot table and fill non existing with high number i.e:100
    pivot = pd.pivot_table(grouped,
                           values='rank',
                           index='Cluster ID',
                           columns=['day'],
                           fill_value=100,
                           aggfunc=np.sum)

    # Aggregate the ranking per day for all the poll period and sort
    agg = pivot.sum(axis=1).sort_values()
    # Series to Dataframe to assign column name
    ranked = pd.DataFrame(agg, columns=['agg_ranking'])
    # join with original data to bring album and artist
    joined = data.join(ranked, on='Cluster ID')
    # Drop duplicates by Cluster ID
    clean = joined[['Cluster ID','album', 'artist', 'agg_ranking']]
    final = clean.drop_duplicates(['Cluster ID']).sort_values('agg_ranking')
    final['rank'] = final["agg_ranking"].rank(
        method='dense').astype(int)
    print final
    # Ouput to csv
    final.to_csv("%s/%s_ranked.csv" % (OUTPUT_PATH, INPUT_FILE), index=False)
    print 'Done.'


if __name__ == '__main__':
    rankEm()
