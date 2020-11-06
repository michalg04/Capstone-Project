import pandas as pd
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
import string
import time

yelp = pd.read_pickle("yelp_geo.p")
rubmaps = pd.read_pickle("rubmaps.p")

# concatenate yelp and rubmaps
concat = pd.concat([yelp, rub], sort=True)
concat = concat.reset_index().drop(["index"], axis = 1)

# round lat/long and create a new variable with both
concat["lon"] = round(concat["lon"].astype(float),5)
concat["lat"] = round(concat["lat"].astype(float),5)
concat['lat_lon'] = list(zip(concat['lat'], concat['lon']))

concat.to_pickle('concat.p')