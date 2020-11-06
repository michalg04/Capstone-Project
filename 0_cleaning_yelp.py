import pandas as pd
import pickle
import json

# get file name from txt file and read in
file_names = open("file_names.txt", "r")
yelp_name = file_names.readlines()[0].strip()
yelp = pd.read_csv(yelp_name)

# pull reviews out of the json
yelp["review_raw"] = yelp["_raw"].apply(lambda x: json.loads(x).get("review"))
yelp["reviews"] = yelp["review_raw"].apply(lambda x: [i.get("description") for i in x])

# combine address information into one clean field
yelp["address.streetAddress"] = yelp["address.streetAddress"].str.replace("\n", " ")
yelp["address.postalCode"] = yelp["address.postalCode"].astype(str).str[:-2]
yelp["address"] = yelp["address.streetAddress"] + ", " + yelp["address.addressRegion"] + ", " + yelp["address.postalCode"]

# determine length of time reviews span
yelp["date"] = yelp['review{}.datePublished'].str.split("\n")
yelp["date"] = yelp["date"].apply(lambda x: [pd.to_datetime(i) for i in x] if type(x) == list else x)
yelp["date_diff"] = yelp["date"].apply(lambda x: max(x) - min(x) if type(x) == list else x)
yelp["range_days"] = yelp["date_diff"].dt.days

# drop unnecessary columns
yelp = yelp.drop(["@context", "_raw", "splunk_server", "splunk_server_group",
              "adLoggingInfo.slot", "adLoggingInfo.placement", "source", "sourcetype",
              "@type", "_time", "verifiedLicenseInfo.licenses{}.issuedBy",
            "verifiedLicenseInfo.licenses{}.licenseNumber",
            "verifiedLicenseInfo.licenses{}.licensee",
           "verifiedLicenseInfo.licenses{}.trade",
           "verifiedLicenseInfo.licenses{}.verifiedDate",
           "verifiedLicenseInfo.bizSiteUrl", "verifiedLicenseInfo.licenses{}.expiryDate",
           "snippet.readMoreUrl", "snippet.thumbnail.src", "snippet.thumbnail.srcset",
           "searchResultBusinessHighlights.businessHighlights{}.title", 
           "searchResultLayoutType", "searchResultLayoutType",
           "searchResultBusinessHighlights.businessHighlights{}.iconName", 
           "searchResultBusinessHighlights.businessHighlights{}.id",
           "searchResultBusinessHighlights.businessHighlights{}.bizPageIconName",
           "searchResultBusinessHighlights.bizSiteUrl"], axis = 1)

# add yelp marker
yelp["yelp"] = 1
yelp["rubmaps"] = 0

pickle.dump(yelp, open( "yelp.p", "wb" ))




