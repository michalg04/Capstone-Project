import urllib.request
import pandas as pd
import json
import time
import unicodedata
import pickle
import sys

df = pickle.load(open("yelp.p", 'rb'))
df = pd.DataFrame(df)

df['lat'] = None
df['lon'] = None

# get google API key from command line argument
if len(sys.argv) <= 1:
    print("Failed: Please supply google API key as a command line argument")
    exit()
else:
    key = sys.argv[1]

for i in df.index:
	try:
        # translate characters to google API-friendly characters
		address = ''.join(
				c for c in unicodedata.normalize('NFD', str(df['address'][i]))
				if unicodedata.category(c) != 'Mn'
		)
		addy = '+'.join(address.split(' '))
        # get latitude and longitude from google
		query = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + addy + '&key=' + key
		with urllib.request.urlopen(query) as response:
			html = response.read()
			y = json.loads(html)['results'][0]['geometry']['location']
			df.at[i, 'lat'] = y['lat']
			df.at[i, 'lon'] = y['lng']
			print("updated to " + str(y['lat']) + ", " + str(y['lng']))
	except: 
        # if failed, fill in with none
		df.at[i, 'lat'] = None
		df.at[i, 'lon'] = None
		print("failed")
	finally:
        # pause to avoid overwhelming computer/google's API
        time.sleep(2)

# fill in values that failed the first time - rerun as necessary
for i in range(len(df['address'])):
    if df['lat'][i] == None or df['lon'][i] == None: 
        try: 
            addy = '+'.join(str(df['address'][i]).split(' '))
            query = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + addy + '&key=' + key
            with urllib.request.urlopen(query) as response:
                html = response.read()
                y = json.loads(html)['results'][0]['geometry']['location']
                df['lat'][i] = y['lat']
                df['lon'][i]= y['lng']
                
        except: 
            pass
        
#manual fixes for lat/long that did not convert correctly
def manual_fix(df):
    # Fix lat long for Face Appeal Beauty Studio
    df.at[5027, 'lat'] = 34.089323
    df.at[5027, 'lon'] = -117.671584
    #Fix lat lon for Sound Touch
    df.at[27906, 'lat'] = 32.982086
    df.at[27906, 'lon'] = -117.270014
    #Fix lat lon for Biatchi, even tho its closed permenently
    df.at[39865, 'lat'] = 34.108276
    df.at[39865, 'lon'] = -117.655003
    #Fix lat lon for Weeds Salon
    df.at[1357, 'lat'] = 37.818698
    df.at[1357, 'lon'] = -122.244440
    #Fix lat lon for Salon Ooh Lala STREET CORNER
    df.at[3489, 'lat'] = 38.678489
    df.at[3489, 'lon'] = -121.271611
    # Fix lat lon for Mommy Who Cuts Hair
    df.at[4646, 'lat'] = 37.730615
    df.at[4646, 'lon'] = -122.160087
    #Fix for Girl Talk Natural Nails and Foot Reflexology
    df.at[5587, 'lat'] = 34.142008
    df.at[5587, 'lon'] = -118.375033
    #Fix for Sports & Neuromuscular Massage Therapy STREET CORNER
    df.at[7226, 'lat'] = 34.053345
    df.at[7226, 'lon'] = -118.376156
    #FIX FOR Eye Candy Salon
    df.at[7911, 'lat'] = 32.712866
    df.at[7911, 'lon'] = -117.155289
    # skin care by zakiya
    df.at[8564, 'lat'] = 37.814305
    df.at[8564, 'lon'] = -121.998357
    # shapes brow bar cart
    df.at[8563, 'lat'] = 37.6506802
    df.at[8563, 'lon'] = -122.1034966
    # dead sexy hair
    df.at[9956, 'lat'] = 34.168680
    df.at[9956, 'lon'] = -118.347139
    # Amy Seo, CMT
    df.at[12402, 'lat'] = 37.780475
    df.at[12402, 'lon'] = -122.475116
    # Studio 56 STREET CORNER
    df.at[13464, 'lat'] = 36.555646
    df.at[13464, 'lon'] = -121.920973
    # CHARLIE BENNETT STREST CORNES
    df.at[15587, 'lat'] = 37.808687
    df.at[15587, 'lon'] = -122.252770
    # Joe Anthony Massage & Bodywork
    df.at[15451, 'lat'] = 37.752808
    df.at[15451, 'lon'] = -122.409141
    # healey touch
    df.at[15776, 'lat'] = 37.533407
    df.at[15776, 'lon'] = -121.920101
    # Bodywork by Egie
    df.at[15822, 'lat'] = 34.019191
    df.at[15822, 'lon'] = -118.478140
    # jennfier
    df.at[17959, 'lat'] = 37.814305
    df.at[17959, 'lon'] = -121.998357
    # Hair by Courtney Canaday
    df.at[17724, 'lat'] = 33.914884
    df.at[17724, 'lon'] = -117.441880
    # salon ciera
    df.at[22049, 'lat'] = 37.973316
    df.at[22049, 'lon'] = -122.526169
    # Raeann Venard Beauty Professional
    df.at[22147, 'lat'] = 39.750379
    df.at[22147, 'lon'] = -121.854467
    # aviante health
    df.at[25342, 'lat'] = 34.180101
    df.at[25342, 'lon'] = -118.864126
    # The Genesis Journy STREET CORNER
    df.at[25551, 'lat'] = 38.705990
    df.at[25551, 'lon'] = -121.327047
    # winzer hair salon
    df.at[29912, 'lat'] = 33.821716
    df.at[29912, 'lon'] = -116.546023
    df.at[25551, 'lon'] = -121.327047
    # sassy nail
    df.at[34286, 'lat'] = 38.730407
    df.at[34286, 'lon'] = -120.786480
    # profiles hair studio
    df.at[34741, 'lat'] = 36.554461
    df.at[34741, 'lon'] = -121.923155
    # Massage by shelley
    df.at[35635, 'lat'] = 39.763591
    df.at[35635, 'lon'] = -121.868634
    # Skincare By Melissa
    df.at[37238, 'lat'] = 33.203381
    df.at[37238, 'lon'] = -117.240730
    # Wellness By Candy
    df.at[39728, 'lat'] = 32.721069
    df.at[39728, 'lon'] = -117.165053
    # zen temple
    df.at[41139, 'lat'] = 37.806205
    df.at[41139, 'lon'] = -122.275947
    # Excellent Touch Massage Therapy
    df.at[43681, 'lat'] = 35.374109
    df.at[43681, 'lon'] = -119.013835
    # best blowouts
    df.at[44010, 'lat'] = 32.602221
    df.at[44010, 'lon'] = -117.064207
    # Domani Salon of Beauty & Wellness
    df.at[46511, 'lat'] = 32.682700
    df.at[46511, 'lon'] = -117.177818
    # bay beauty
    df.at[54479, 'lat'] = 35.369168
    df.at[54479, 'lon'] = -120.854049
    return df

# by default, drop observations with lat/long outside california
# can add a -m flag to perform the manual cleaning we did on these observations
if len(sys.argv) > 2 and sys.argv[2] == "-m":
    df = manual_fix(df)
else:
    dropped = sum(df["lat"].astype(float) > 41.995237)
    df = df[df["lat"].astype(float) <= 41.995237]
    dropped += sum(df["lon"].astype(float) > -114.133039)
    df = df[df["lon"].astype(float) <= -114.133039]
    print("Dropped " + str(dropped) + " observations with lat/lon outside California")

# drop rows with null addresses, lats, or longs
df = df[df.address.notna()]
df = df[df.lat.notna()]
df = df[df.lon.notna()]
df = df.reset_index(drop=True)

# reshape the dataframe to have one row for each review
df['reviews'] = df['reviews'].apply(lambda x: ast.literal_eval(x))
df = df.explode('reviews')

# subset dataframe to merge with rubmaps
df = df[['name', "address", "reviews","range_days",
              'lat', 'lon', 'yelp', 'rubmaps']].rename(columns={"reviews":"review"})

pickle.dump(df, open( "yelp_geo.p", "wb" ))