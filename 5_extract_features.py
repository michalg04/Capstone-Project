import pandas as pd
import numpy as np
import time
import sys
import re
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sys

# get file name from txt file and read in
file_names = open("file_names.txt", "r").readlines()
lex_name = file_names[3].strip()

lex = pd.read_csv(lex_name).dropna().rename(columns={
    'Human Trafficking (weight 0-1-2)':'HT_Weight',"Test Weight (0-1-2)":"Sex_Weight"})

# organize lexicon into dictionaries for sex and human trafficking
ht_dict = pd.Series(lex.HT_Weight.values, index=lex.TERM)
sex_dict = pd.Series(lex.Sex_Weight.values, index=lex.TERM)

ht_dict = ht_dict.reset_index()
ht_dict['TERM'] = ht_dict['TERM'].apply(lambda x: x.lower())
ht_dict.index = ht_dict["TERM"]
ht_dict = ht_dict.drop("TERM", axis=1)
ht_dict = ht_dict.to_dict()[0]

sex_dict = sex_dict.reset_index()
sex_dict['TERM'] = sex_dict['TERM'].apply(lambda x: x.lower())
sex_dict.index = sex_dict["TERM"]
sex_dict = sex_dict.drop("TERM", axis=1)
sex_dict = sex_dict.to_dict()[0]

# compute lexicon scores, unigrams, bigrams, trigrams for each review
def lex_score(row):
    ht_0 = []
    ht_1 = []
    ht_2 = []
    sex_0 = []
    sex_1 = []
    sex_2 = []

    if(pd.notnull(row['clean_reviews'])):
        for term in ht_dict.keys():
            term_padded = " " + re.escape(term) + " "
            row_padded = " " + row['clean_reviews'] + " "
            indices = [(m.start(), m.end()) for m in re.finditer(term_padded, row_padded)]
            if indices != []:
                if ht_dict[term] == 0:
                    ht_0.extend(indices)
                elif ht_dict[term] == 1:
                    ht_1.extend(indices)
                elif ht_dict[term] == 2:
                    ht_2.extend(indices)
                    
                if sex_dict[term] == 0:
                    sex_0.extend(indices)
                elif sex_dict[term] == 1:
                    sex_1.extend(indices)
                elif sex_dict[term] == 2:
                    sex_2.extend(indices)   
                    
    ht_0.sort(key=lambda x: x[0])
    ht_1.sort(key=lambda x: x[0])
    ht_2.sort(key=lambda x: x[0])
    
    sex_0.sort(key=lambda x: x[0])
    sex_1.sort(key=lambda x: x[0])
    sex_2.sort(key=lambda x: x[0])
    
    HT_uni_0_count = len(ht_0)
    HT_uni_1_count = len(ht_1)
    HT_uni_2_count = len(ht_2)
    sex_uni_0_count = len(sex_0)
    sex_uni_1_count = len(sex_1)
    sex_uni_2_count = len(sex_2)
    
    HT_bi_0_count = count_bigrams(ht_0)
    HT_bi_1_count = count_bigrams(ht_1)
    HT_bi_2_count = count_bigrams(ht_2)
    HT_tri_0_count = count_trigrams(ht_0)
    HT_tri_1_count = count_trigrams(ht_2)
    HT_tri_2_count = count_trigrams(ht_2)

    sex_bi_0_count = count_bigrams(sex_0)
    sex_bi_1_count = count_bigrams(sex_1)
    sex_bi_2_count = count_bigrams(sex_2)
    sex_tri_0_count = count_trigrams(sex_0)
    sex_tri_1_count = count_trigrams(sex_1)
    sex_tri_2_count = count_trigrams(sex_2)
    
    row['HT_bi_0_count'] = HT_bi_0_count
    row['HT_bi_1_count'] = HT_bi_1_count
    row['HT_bi_2_count'] = HT_bi_2_count
    row['HT_tri_0_count'] = HT_tri_0_count
    row['HT_tri_1_count'] = HT_tri_1_count
    row['HT_tri_2_count'] = HT_tri_2_count
    row['HT_uni_0_count'] = HT_uni_0_count
    row['HT_uni_1_count'] = HT_uni_1_count
    row['HT_uni_2_count'] = HT_uni_2_count
    
    row['sex_bi_0_count'] = sex_bi_0_count
    row['sex_bi_1_count'] = sex_bi_1_count
    row['sex_bi_2_count'] = sex_bi_2_count
    row['sex_tri_0_count'] = sex_tri_0_count
    row['sex_tri_1_count'] = sex_tri_1_count
    row['sex_tri_2_count'] = sex_tri_2_count
    row['sex_uni_0_count'] = sex_uni_0_count
    row['sex_uni_1_count'] = sex_uni_1_count
    row['sex_uni_2_count'] = sex_uni_2_count
    
    return row

# helper function to count bigrams
def count_bigrams(l):
    bis = 0
    for i in range(len(l) - 1):
        # if end of current overlaps with start of next
        if l[i][1] >= l[i+1][0]:
            bis += 1
    return bis

# helper function to count trigrams
def count_trigrams(l):
    tris = 0
    for i in range(len(l) - 2):
        # if end of current overlaps with start of next and end of next 
        # overlaps start of next next
        if l[i][1] >= l[i+1][0] and l[i+1][1] >= l[i+2][0]:
            tris += 1
    return tris

# run K-Means clustering on a dataset and assign each row to one of two clusters
def add_cluster(df):
    grouped = df.groupby(['norm_id']).agg({"yelp": "sum",
                              "rubmaps":"sum", "name": lambda x: list(set(x)),
                                 "address":lambda x: list(set(x)),
                                 'HT_bi_0_count':"max",
    'HT_bi_1_count':"max", 'HT_bi_2_count':"max", 'HT_tri_0_count':"max", 'HT_tri_1_count':"max",
    'HT_tri_2_count':"max", 'HT_uni_0_count':"max", 'HT_uni_1_count':"max", 'HT_uni_2_count':"max",
    'sex_bi_0_count':"max", 'sex_bi_1_count':"max", 'sex_bi_2_count':"max", 'sex_tri_0_count':"max",
    'sex_tri_1_count':"max", 'sex_tri_2_count':"max", 'sex_uni_0_count':"max",
    'sex_uni_1_count':"max", 'sex_uni_2_count':"max"})
    grouped['num_names'] = grouped['name'].apply(lambda x: len(x))
    grouped['num_addresses'] = grouped['address'].apply(lambda x: len(x))

    X = grouped.loc[:, ['yelp', 'rubmaps', 'HT_bi_0_count',
       'HT_bi_1_count', 'HT_bi_2_count', 'HT_tri_0_count', 'HT_tri_1_count',
       'HT_tri_2_count', 'HT_uni_0_count', 'HT_uni_1_count', 'HT_uni_2_count',
       'sex_bi_0_count', 'sex_bi_1_count', 'sex_bi_2_count', 'sex_tri_0_count',
       'sex_tri_1_count', 'sex_tri_2_count', 'sex_uni_0_count',
       'sex_uni_1_count', 'sex_uni_2_count']]
    # standardize data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    # form the clusters
    cl = KMeans(n_clusters=2).fit(X)
    # add clusters to dataframe
    grouped['cluster'] = cl.labels_
    grouped = grouped.drop(['address', 'name', 'rubmaps', 'yelp',
           'HT_bi_0_count', 'HT_bi_1_count', 'HT_bi_2_count', 'HT_tri_0_count',
           'HT_tri_1_count', 'HT_tri_2_count', 'HT_uni_0_count', 'HT_uni_1_count',
           'HT_uni_2_count', 'sex_bi_0_count', 'sex_bi_1_count', 'sex_bi_2_count',
           'sex_tri_0_count', 'sex_tri_1_count', 'sex_tri_2_count',
           'sex_uni_0_count', 'sex_uni_1_count', 'sex_uni_2_count', 'num_names','num_addresses'], axis = 1)
    df_with_clusters = df.merge(grouped, on='norm_id')
    return df_with_clusters

ca_reviews = pd.read_pickle('cleaned_reviews.p')

# read in florida reviews and combine with their names
# get file names from txt file
file_names = open("file_names.txt", "r")
fl_name = file_names[4].strip()
fl_address_name = file_names[5].strip()
fl = pd.read_csv(fl_name)
fl_info = pd.read_csv(fl_address_name)[['id', 'address','business_license_name']]
fl = fl.merge(fl_info, how="left", left_on="norm_id", right_on="id")
fl['business_license_name'].replace(np.nan, "", regex=True, inplace=True)
fl['business_license_name'] = fl['business_license_name'].astype(str)

fl_reviews = fl.rename(columns={'business_license_name':'name'})

# add yelp/rubmaps flags to florida data
fl_reviews['rubmaps'] = fl_reviews['rm_review_flag'].apply(lambda x: 0 if x=='N' else 1)
fl_reviews['yelp'] = fl_reviews['yelp_review_flag'].apply(lambda x: 0 if x=='N' else 1) 

ca_reviews = add_cluster(ca_reviews.apply(lex_score, axis=1))
fl_reviews = add_cluster(fl_reviews.apply(lex_score, axis=1))

ca_reviews.to_pickle('ca_final.p')
fl_reviews.to_pickle('fl_final.p')
