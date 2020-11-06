import nltk
from nltk.corpus import stopwords
import pandas as pd
import string
import time

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
    df['clean_reviews'] = df.apply(clean_review, axis=1)
    df.to_pickle('review_cleaned.p')
    runtime = time.time() - start_time
    with open("cleaning_runtime.txt", 'w') as file:
        file.write(str(runtime))

if __name__ == "__main__":
    clean()
