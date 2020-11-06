import pandas as pd

# get file name from txt file and read in
file_names = open("file_names.txt", "r").readlines()
CA_name = file_names[1].strip()
null_name = file_names[2].strip()
ca = pd.read_csv(CA_name)
null_states = pd.read_csv(null_name)

# combine businesses listed as California with those listed as null, but in CA
ca_null = null_states[null_states["address"].str.contains("CA", case = True)]
bad_rows = []
for row in list(ca_null["address"]):
    if (row.split(","))[-2] != " CA":
        bad_rows.append(row)
ca_null = ca_null[~ca_null["address"].isin(bad_rows)]
ca_full = pd.concat([ca, ca_null]).reset_index(drop=True)

# drop unnecessary columns
ca_clean = ca_full.drop(['@timestamp', '@version', '_raw', 'address_soundex',
       'addresses{}', 'city', 'county', 'cribl','cribl_pipe', 'imb_urls{}',
              "linecount",'location_hash', 'location_id','source_id',
              'sourcetype', 'splunk_server', 'splunk_server_group',"host", "index",
       'state', 'source', "zip"], axis = 1)

# add rubmaps marker
ca_clean["yelp"] = 0
ca_clean["rubmaps"] = 1

# choose final columns and rename them to better combine with yelp data
ca_clean = ca_clean[['name{}', 'address', "more_details", 'geo.lat', 'geo.lon',
              'yelp', 'rubmaps']].rename(columns={'name{}': 'name','geo.lat':'lat',
                                                  'geo.lon':'lon', "more_details":"review"})

ca_clean.to_pickle("rubmaps.p")
