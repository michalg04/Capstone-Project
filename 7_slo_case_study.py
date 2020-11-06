import pandas as pd
import numpy as np
import sys

# read in files
file_names = open("file_names.txt", "r")
ca_name = file_names.readlines()[6].strip()

ca_pred = pd.read_pickle(ca_name)
ca_add = pd.read_pickle('ca_final.p')
zips = pd.read_csv('SLO_zips.csv')
zips = list(zips['Zip Code'])

ca = ca_add.merge(ca_pred, on="norm_id")

# extract zip codes from dataset
ca['zip'] = ca['address'].str.split(',').apply(lambda x: x[-1])
ca['zip'] = ca['zip'].apply(pd.to_numeric, args=('coerce',))
ca = ca[ca['zip'].notna()]
ca['zip'] = ca['zip'].astype(int)

# get only businesses with SLO zip codes
ca['slo'] = ca['zip'].apply(lambda x: 1 if x in zips else 0)

ca_group = ca.groupby('norm_id').agg({"lat":'max', "lon":'max', "yelp": "sum",
                                  "rubmaps":"sum", "name": lambda x: list(set(x)),
                                     "address":lambda x: list(set(x)),
                                     'HT_bi_0_count':"max",
       'HT_bi_1_count':"max", 'HT_bi_2_count':"max", 'HT_tri_0_count':"max", 'HT_tri_1_count':"max",
       'HT_tri_2_count':"max", 'HT_uni_0_count':"max", 'HT_uni_1_count':"max", 'HT_uni_2_count':"max",
       'sex_bi_0_count':"max", 'sex_bi_1_count':"max", 'sex_bi_2_count':"max", 'sex_tri_0_count':"max",
       'sex_tri_1_count':"max", 'sex_tri_2_count':"max", 'sex_uni_0_count':"max",
       'sex_uni_1_count':"max", 'sex_uni_2_count':"max", 'range_days':'max','slo':'max',
                                      'pred':'max'})
ca_group = ca_group[ca_group['slo']==1]

# create a table of only SLO businesses with risk scores >=0.5
high_risk = ca_group[ca_group['pred']>=0.5].reset_index()
df = high_risk[['name','address','pred']]

# manually clean up SLO business table
def manual_fix(df):
    df = df.drop(16).explode('name').drop(4)
    df['name'] = df['name'].apply(lambda x: x.split('\n'))
    df = df.explode('name').reset_index()
    df = df.drop('index',axis=1).sort_values('name')
    df = df.drop([6,0,8,5,33])
    df = df.explode('address').sort_values('address').reset_index()
    df = df.drop('index',axis=1).drop([29,31,32]).reset_index()
    df = df.drop('index',axis=1)
    df.at[31,'pred'] = 0.954953
    df = df.drop(30)
    return df

# by default, does not perform our manual cleaning
# add -m flag to use our manual clean function
if len(sys.argv) > 1 and sys.argv[1] == "-m":
    df = manual_fix(df)

df = df.sort_values('pred', ascending=False)

df.to_csv('slo_IMBs.csv')
