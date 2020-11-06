import pandas as pd
import pickle
import json

yelp = pd.read_pickle("yelp_raw.p")
df = pd.read_csv("null_states.csv")
CA_og = pd.read_csv("CA_rubmaps.csv")
female_names  = list(pd.read_csv("female.firstnames.csv", header = None)[0])

# clean yelp
yelp.reset_index(inplace=True, drop=True)
yelp["review_raw"] = yelp["_raw"].apply(lambda x: json.loads(x).get("review"))
yelp["reviews"] = yelp["review_raw"].apply(lambda x: [i.get("description") for i in x])
yelp = yelp.drop(["@context", "_raw", "splunk_server", "splunk_server_group",
  "adLoggingInfo.slot", "adLoggingInfo.placement", "source", "sourcetype"], axis = 1)
yelp["address.streetAddress"] = yelp["address.streetAddress"].str.replace("\n", " ")
yelp["address.postalCode"] = yelp["address.postalCode"].astype(str).str[:-2]
yelp["address"] = yelp["address.streetAddress"] + ", " +
 yelp["address.addressRegion"] + ", " + yelp["address.postalCode"]
pickle.dump(yelp, open( "yelp.p", "wb" ))

# clean rubmaps
CA_df = df[df["address"].str.contains("CA", case = True)]
bad_rows = []
for row in list(CA_df["address"]):
    if (row.split(","))[-2] != " CA":
        bad_rows.append(row)
CA_df = CA_df[~CA_df["address"].isin(bad_rows)]
ca_full = pd.concat([CA_og, CA_df]).reset_index(drop=True)
ca_clean = ca_full.drop(['@timestamp', '@version', '_raw', 'address_soundex',
       'addresses{}', 'city', 'county', 'cribl','cribl_pipe', 'imb_urls{}',
              "linecount",'location_hash', 'location_id','source_id',
              'sourcetype', 'splunk_server', 'splunk_server_group',"host", "index",
       'state', 'source', "zip"], axis = 1)
ca_clean.to_csv("CA_final.csv", index = False)

# attempted work with rubmaps names
def get_key(val): 
    for key, value in d.items(): 
         if val == value: 
            return key 
  
    return "key doesn't exist"
names = []
for name in female_names:
    if type(name) is str:
        if len(name) > 2:
            names.append(name)
names = [e for e in names if e not in ["SEE", "MANY", "LADY", "MISS", "LATINA",
  "SOON", "LATINA", "YOUNG", "LOVE", "MAN", "ELSE"]]
names_d = {}
for index in list(d.keys()):
    details = d.get(index)
    if type(details) is str:
        names_per_details = []
        for word in details.upper().split():
            if word in names:
                if word not in names_per_details:
                        names_per_details.append(word) 
    if len(names_per_details) > 0:
        names_d[index] = names_per_details
ca_clean[ca_clean.index.isin(names_d.keys())]["worker.name"] = list(names_d.values())
for index in names_d.keys():
    ca_clean.at[index, "worker.name"] = names_d.get(index)
        
              

