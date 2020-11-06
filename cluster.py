import pickle
import time
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def main(infile, outfile):
    grouped = df.groupby(['norm_id']).agg({"yelp": "sum",
                              "rubmaps":"sum", "name": lambda x: list(set(x)),
                                 "address":lambda x: list(set(x)),
                                 'HT_bi_0_count':"max",
   'HT_bi_1_count':"max", 'HT_bi_2_count':"max", 'HT_tri_0_count':"max", 'HT_tri_1_count':"max",
   'HT_tri_2_count':"max", 'HT_uni_0_count':"max", 'HT_uni_1_count':"max", 'HT_uni_2_count':"max",
   'sex_bi_0_count':"max", 'sex_bi_1_count':"max", 'sex_bi_2_count':"max", 'sex_tri_0_count':"max",
   'sex_tri_1_count':"max", 'sex_tri_2_count':"max", 'sex_uni_0_count':"max",
   'sex_uni_1_count':"max", 'sex_uni_2_count':"max"})
    print('grouped')
    grouped['num_names'] = grouped['name'].apply(lambda x: len(x))
    grouped['num_addresses'] = grouped['address'].apply(lambda x: len(x))

    X = grouped.loc[:, ['yelp', 'rubmaps', 'HT_bi_0_count',
       'HT_bi_1_count', 'HT_bi_2_count', 'HT_tri_0_count', 'HT_tri_1_count',
       'HT_tri_2_count', 'HT_uni_0_count', 'HT_uni_1_count', 'HT_uni_2_count',
       'sex_bi_0_count', 'sex_bi_1_count', 'sex_bi_2_count', 'sex_tri_0_count',
       'sex_tri_1_count', 'sex_tri_2_count', 'sex_uni_0_count',
       'sex_uni_1_count', 'sex_uni_2_count']]
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    print('standardized')
    cl = KMeans(n_clusters=2).fit(X)
    grouped['cluster'] = cl.labels_
    grouped = grouped.drop(['address', 'name', 'rubmaps', 'yelp',
           'HT_bi_0_count', 'HT_bi_1_count', 'HT_bi_2_count', 'HT_tri_0_count',
           'HT_tri_1_count', 'HT_tri_2_count', 'HT_uni_0_count', 'HT_uni_1_count',
           'HT_uni_2_count', 'sex_bi_0_count', 'sex_bi_1_count', 'sex_bi_2_count',
           'sex_tri_0_count', 'sex_tri_1_count', 'sex_tri_2_count',
           'sex_uni_0_count', 'sex_uni_1_count', 'sex_uni_2_count', 'num_names','num_addresses'], axis = 1)
    df_with_clusters = df.merge(grouped, on='norm_id').drop(['g_id', 'lat_lon'], axis=1)
    df_with_clusters.to_pickle(outfile)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "input-filename output-filename.p")
        exit()
    start_time = time.time()
    main(sys.argv[1], sys.argv[2])
    runtime = time.time() - start_time
    with open('cluster_rutime.txt', 'w') as file:
        file.write(str(runtime))
