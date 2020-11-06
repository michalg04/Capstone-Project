import pandas as pd
import numpy as np
import ast
import pickle

yelp2 = pd.read_pickle("yelp_2.p")
rubmaps = pd.read_csv("rubmaps_final.csv")

yelp2["date"] = yelp2['review{}.datePublished'].str.split("\n")
yelp2["date"] = yelp2["date"].apply(lambda x: [pd.to_datetime(i) for i in x] if type(x) == list else x)

# add feature for number of days of reviews
yelp2["date_diff"] = yelp2["date"].apply(lambda x: max(x) - min(x) if type(x) == list else x)
yelp2["range_days"] = yelp2["date_diff"].dt.days

yelp2 = yelp2.drop(["@type", "_time", "verifiedLicenseInfo.licenses{}.issuedBy",
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

# fix lat and long
yelp2["lat_lon"] = yelp2.lat.astype(str) + ", " + yelp2.long.astype(str)
rubmaps["lat_lon"] = rubmaps["geo.lat"].astype(str) + ", " + rubmaps["geo.lon"].astype(str)
yelp2["lon"] = round(yelp2["long"].astype(float),4)
yelp2["lat_2"] = yelp2["lat"].astype(float)
# Fix lat long for Face Appeal Beauty Studio
yelp2.at[5027, 'lat_2'] = 34.089323
yelp2.at[5027, 'lon'] = -117.671584
#Fix lat lon for Sound Touch
yelp2.at[27906, 'lat_2'] = 32.982086
yelp2.at[27906, 'lon'] = -117.270014
#Fix lat lon for Biatchi, even tho its closed permenently
yelp2.at[39865, 'lat_2'] = 34.108276
yelp2.at[39865, 'lon'] = -117.655003
#Fix lat lon for Weeds Salon
yelp2.at[1357, 'lat_2'] = 37.818698
yelp2.at[1357, 'lon'] = -122.244440
#Fix lat lon for Salon Ooh Lala STREET CORNER
yelp2.at[3489, 'lat_2'] = 38.678489
yelp2.at[3489, 'lon'] = -121.271611
# Fix lat lon for Mommy Who Cuts Hair
yelp2.at[4646, 'lat_2'] = 37.730615
yelp2.at[4646, 'lon'] = -122.160087
#Fix for Girl Talk Natural Nails and Foot Reflexology
yelp2.at[5587, 'lat_2'] = 34.142008
yelp2.at[5587, 'lon'] = -118.375033
#Fix for Sports & Neuromuscular Massage Therapy STREET CORNER
yelp2.at[7226, 'lat_2'] = 34.053345
yelp2.at[7226, 'lon'] = -118.376156
#FIX FOR Eye Candy Salon
yelp2.at[7911, 'lat_2'] = 32.712866
yelp2.at[7911, 'lon'] = -117.155289
# skin care by zakiya
yelp2.at[8564, 'lat_2'] = 37.814305
yelp2.at[8564, 'lon'] = -121.998357
# shapes brow bar cart
yelp2.at[8563, 'lat_2'] = 37.6506802
yelp2.at[8563, 'lon'] = -122.1034966
# dead sexy hair
yelp2.at[9956, 'lat_2'] = 34.168680
yelp2.at[9956, 'lon'] = -118.347139
# Amy Seo, CMT
yelp2.at[12402, 'lat_2'] = 37.780475
yelp2.at[12402, 'lon'] = -122.475116
# Studio 56 STREET CORNER AND PERMAMNETLY CLOSED
yelp2.at[13464, 'lat_2'] = 36.555646
yelp2.at[13464, 'lon'] = -121.920973
# CHARLIE BENNETT STREST CORNES
yelp2.at[15587, 'lat_2'] = 37.808687
yelp2.at[15587, 'lon'] = -122.252770
# Joe Anthony Massage & Bodywork
yelp2.at[15451, 'lat_2'] = 37.752808
yelp2.at[15451, 'lon'] = -122.409141
# healey touch
yelp2.at[15776, 'lat_2'] = 37.533407
yelp2.at[15776, 'lon'] = -121.920101
# Bodywork by Egie
yelp2.at[15822, 'lat_2'] = 34.019191
yelp2.at[15822, 'lon'] = -118.478140
# jennfier
yelp2.at[17959, 'lat_2'] = 37.814305
yelp2.at[17959, 'lon'] = -121.998357
# Hair by Courtney Canaday
yelp2.at[17724, 'lat_2'] = 33.914884
yelp2.at[17724, 'lon'] = -117.441880
# salon ciera
yelp2.at[22049, 'lat_2'] = 37.973316
yelp2.at[22049, 'lon'] = -122.526169
# Raeann Venard Beauty Professional
yelp2.at[22147, 'lat_2'] = 39.750379
yelp2.at[22147, 'lon'] = -121.854467
# aviante health
yelp2.at[25342, 'lat_2'] = 34.180101
yelp2.at[25342, 'lon'] = -118.864126
# The Genesis Journy STREET CORNER
yelp2.at[25551, 'lat_2'] = 38.705990
yelp2.at[25551, 'lon'] = -121.327047
# winzer hair salon
yelp2.at[29912, 'lat_2'] = 33.821716
yelp2.at[29912, 'lon'] = -116.546023
yelp2.at[25551, 'lon'] = -121.327047
# sassy nail
yelp2.at[34286, 'lat_2'] = 38.730407
yelp2.at[34286, 'lon'] = -120.786480
# profiles hair studio
yelp2.at[34741, 'lat_2'] = 36.554461
yelp2.at[34741, 'lon'] = -121.923155
# Massage by shelley
yelp2.at[35635, 'lat_2'] = 39.763591
yelp2.at[35635, 'lon'] = -121.868634
# Skincare By Melissa
yelp2.at[37238, 'lat_2'] = 33.203381
yelp2.at[37238, 'lon'] = -117.240730
# Wellness By Candy
yelp2.at[39728, 'lat_2'] = 32.721069
yelp2.at[39728, 'lon'] = -117.165053
# zen temple
yelp2.at[41139, 'lat_2'] = 37.806205
yelp2.at[41139, 'lon'] = -122.275947
# ANGEL TOUCH THERAPUTIC MASSAGE IS PROLLY GONNA GET DROPPED
# Excellent Touch Massage Therapy
yelp2.at[43681, 'lat_2'] = 35.374109
yelp2.at[43681, 'lon'] = -119.013835
# best blowouts
yelp2.at[44010, 'lat_2'] = 32.602221
yelp2.at[44010, 'lon'] = -117.064207
# Domani Salon of Beauty & Wellness
yelp2.at[46511, 'lat_2'] = 32.682700
yelp2.at[46511, 'lon'] = -117.177818
# bay beauty
yelp2.at[54479, 'lat_2'] = 35.369168
yelp2.at[54479, 'lon'] = -120.854049

# prepare for merge
yelp_revs = pd.read_csv("yelp_reviews_list.csv", index_col=0)
yelp2 = yelp2.join(yelp_revs)
yelp2 = yelp2[yelp2.address.notna()]
yelp2["lat_lon"] = yelp2.lat_2.astype(str) + ", " + yelp2.lon.astype(str)
rubmaps["lat_lon"] = rubmaps["geo.lat"].astype(str) + ", " + rubmaps["geo.lon"].astype(str)
yelp2["yelp"] = 1
yelp2["rubmaps"] = 0
rubmaps["yelp"] = 0
rubmaps["rubmaps"] = 1
yelp2['reviews'] = yelp2['reviews'].apply(lambda x: ast.literal_eval(x))
yelp2 = yelp2.explode('reviews')
yelp = yelp2[['name', "address", "reviews","range_days",
              'lat_2', 'lon', 'yelp', 'rubmaps']].rename(columns={'lat_2': 'lat', "reviews":"review"})

# fix null lat/long for yelp
y_null = yelp[yelp["lat"].isna()]
null_indexes = list(y_null.index)
yelp = yelp.drop(null_indexes)
y_fixed = pd.read_csv("completed_yelp.csv")
y_fixed = y_fixed.set_index("Unnamed: 0")
y_fixed.index.name = None
# Adam Atman
y_fixed.at[19735, 'lat'] = 37.220500
y_fixed.at[19735, 'lon'] = -121.986011
# Red Persimmon Nails & Spa
y_fixed.at[35939, 'lat'] = 33.876055 
y_fixed.at[35939, 'lon'] = -118.219873
#Know Knots Massage
y_fixed.at[54944, 'lat'] = 33.959429
y_fixed.at[54944, 'lon'] = -117.331608
y_fixed.at[56777, 'lat'] = 33.959429
y_fixed.at[56777, 'lon'] = -117.331608
y_fixed = y_fixed.drop([40037,47460])
yelp = pd.concat([yelp, y_fixed], sort=True)

# concatenate!
rub =rubmaps[['name{}', 'address', "more_details", 'geo.lat', 'geo.lon',
              'yelp', 'rubmaps']].rename(columns={'name{}': 'name','geo.lat':'lat',
                                                  'geo.lon':'lon', "more_details":"review"})
concat = pd.concat([yelp, rub], sort=True)
concat = concat.reset_index().drop(["index"], axis = 1)
concat["lon"] = round(concat["lon"].astype(float),5)
concat["lat"] = round(concat["lat"].astype(float),5)
concat['lat_lon'] = list(zip(concat['lat'], concat['lon']))
pickle.dump(concat, open( "concat.p", "wb" ))
