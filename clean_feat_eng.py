import nltk
from nltk.corpus import stopwords
import pandas as pd
import string
import time
import numpy as np
import re

lex = pd.read_csv("Trafficking_Lexicon.csv").dropna().rename(columns={'Human Trafficking (weight 0-1-2)':'HT_Weight',
                                                                     "Test Weight (0-1-2)":"Sex_Weight"})
ht_dict = pd.Series(lex.HT_Weight.values, index=lex.TERM)
sex_dict = pd.Series(lex.Sex_Weight.values, index=lex.TERM)

ht_dict = ht_dict.reset_index()
ht_dict['TERM'] = ht_dict['TERM'].apply(lambda x: x.lower())
ht_dict.index = ht_dict["TERM"]
ht_dict = ht_dict.drop("TERM", axis=1)
ht_dict = ht_dict.to_dict()[0]

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

def clean():
    start_time = time.time()

    df = pd.read_pickle('concat.p')

    #df_sub = df.iloc[:20].copy()
    df['review'] = df.apply(clean_review, axis=1)
    df.to_pickle('review_cleaned.p')
    runtime = time.time() - start_time
    with open("cleaning_runtime.txt", 'w') as file:
        file.write(str(runtime))

lex = pd.read_csv("Trafficking_Lexicon.csv").dropna().rename(columns={'Human Trafficking (weight 0-1-2)':'HT_Weight',
                                                                     "Test Weight (0-1-2)":"Sex_Weight"})
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

def lex_score(row):
    ht_0 = []
    ht_1 = []
    ht_2 = []
    sex_0 = []
    sex_1 = []
    sex_2 = []

    if(pd.notnull(row['review'])):
        for term in ht_dict.keys():
            term_padded = " " + re.escape(term) + " "
            row_padded = " " + row['review'] + " "
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

def count_bigrams(l):
    bis = 0
    for i in range(len(l) - 1):
        # if end of current overlaps with start of next
        if l[i][1] >= l[i+1][0]:
            bis += 1
    return bis

def count_trigrams(l):
    tris = 0
    for i in range(len(l) - 2):
        # if end of current overlaps with start of next and end of next 
        # overlaps start of next next
        if l[i][1] >= l[i+1][0] and l[i+1][1] >= l[i+2][0]:
            tris += 1
    return tris

def extract():
    start_time = time.time()

    reviews = pd.read_pickle("review_cleaned.p")

    reviews = reviews.apply(lex_score, axis=1)
    reviews.to_pickle('review_features.p')
    runtime = time.time() - start_time
    with open("features_runtime.txt", 'w') as file:
        file.write(str(runtime))

clean()
extract()