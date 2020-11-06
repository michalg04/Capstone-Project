import pandas as pd
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
import string
import sys

# get file name from txt file and read in
file_names = open("file_names.txt", "r")
lex_name = file_names.readlines()[3].strip()

lex = pd.read_csv(lex_name).dropna().rename(columns={
    'Human Trafficking (weight 0-1-2)':'HT_Weight',"Test Weight (0-1-2)":"Sex_Weight"})
concat = pd.read_pickle('concat.p')

# reorganize the lexicon to be more useful
ht_dict = pd.Series(lex.HT_Weight.values, index=lex.TERM)
ht_dict = ht_dict.reset_index()
ht_dict['TERM'] = ht_dict['TERM'].apply(lambda x: x.lower())
ht_dict.index = ht_dict["TERM"]
ht_dict = ht_dict.drop("TERM", axis=1)
ht_dict = ht_dict.to_dict()[0]

# clean review by removing stop words and dropping unnecessary punctuation
sw = set(stopwords.words('english'))
table = str.maketrans('', '', string.punctuation)

def clean_review(review):
    text = review['review']
    fin_text = []
    if(pd.notnull(text)):
        for word in text.split():
            l_word = word.lower()
            if l_word not in sw or l_word in ht_dict.keys():
                fin_text.append(l_word.translate(table))
    return " ".join(fin_text)

concat['clean_reviews'] = concat.apply(clean_review, axis=1)

# combine lat/long pair into a string, with a suite number if applicable
regs = [r'(?:ste|unit)\W+([\w-]+)\W',
       r'studio\W+([\w-]+)\W',
       r'#\W*([\w-]+)\W']
def stringify_key(row):
    lat_lon_pair = "{:.5f}".format(row.lat) + ":" + "{:.5f}".format(row.lon) + "#"
    address = row.address.lower()
    for reg in regs:
        match = re.search(reg, address)
        if match:
            return lat_lon_pair + match.groups(0)[0]
    return lat_lon_pair

# combine reviews with lat/long pairs that are the same or very close
def fuzzy_latlon(df, epsilon=0.0001):
    df_new = df.sort_values(by=['lat','lon'])
    df_new = df_new.reset_index().drop(["index"], axis = 1)
    g_id = 0
    df_new['g_id'] = -1
    j = 0
    for i in range(len(df) - 1):
        if i >= j:
            old = df_new.iloc[i]['lat_lon']
            df_new.at[i, 'g_id'] = g_id
            j = i + 1
            while similar(df_new.iloc[j]['lat_lon'],old,epsilon):
                df_new.at[j, 'g_id'] = g_id
                j += 1
                if (j >= (len(df)-1)):
                    break
            g_id += 1
    return df_new

# helper function to determine if lat/long pairs is 'close enough'
def similar(t1, t2, epsilon):
    diff1 = abs(t1[0] - t2[0])
    diff2 = abs(t1[1] - t2[1])
    if (diff1 <= epsilon) and (diff2 <= epsilon):
        return True
    else:
        return False
    
fuz = fuzzy_latlon(concat)

# group reviews together by lat/long id to get uniform lat/long numbers
grouped = fuz.groupby(['g_id']).agg({"lat":'max', "lon":'max'})

# add the uniform lat/long numbers to the original dataset
df = pd.merge(fuz, grouped, on='g_id').drop(['lat_x', 'lon_x'], axis=1)
df = df.rename(columns={'lat_y':'lat', 'lon_y':'lon'})

# create our real final IDs including uniform lat/long and suite number if applicable
df['norm_id'] = df.apply(stringify_key, axis=1)

df.to_pickle('cleaned_reviews.p')
