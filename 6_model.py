import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers, optimizers
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

ca = pd.read_pickle("ca_final.p")
fl = pd.read_pickle("fl_final.p")

features = ['HT_bi_0_count', 'HT_bi_1_count', 'HT_bi_2_count',
       'HT_tri_0_count', 'HT_tri_1_count',
       'HT_tri_2_count', 'HT_uni_0_count', 'HT_uni_1_count', 'HT_uni_2_count',
       'sex_bi_0_count', 'sex_bi_1_count',
       'sex_bi_2_count',  'sex_tri_0_count',
       'sex_tri_1_count', 'sex_tri_2_count', 'sex_uni_0_count',
       'sex_uni_1_count', 'sex_uni_2_count', 'yelp', 'rubmaps', 'cluster']

# combine dataframes
sup1 = fl[features]
sup1['state'] = "FL"
sup2 = ca[features]
sup2['state'] = "CA"
sup = pd.concat([sup1,sup2])

# standardize together
sc = MinMaxScaler()
sup_st = sc.fit_transform(sup[features].values)

# split dataframes back up
sup_f = pd.DataFrame(sup_st, columns=features)
sup_f['state'] = sup['state'].values
florida = sup_f[sup_f['state']=="FL"]
california = sup_f[sup_f['state']=="CA"]

# train test split
X = florida[features].values
y = fl[["prob"]].values
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.25)

# set up and run model
model = Sequential()
model.add(Dense(20))
model.add(Dense(1, activation="sigmoid"))
opt = keras.optimizers.Adam(lr=0.0001)
model.compile(loss='mse', optimizer=opt)
model.fit(X_train, y_train, epochs=20, batch_size=100)

# compute florida accuracy
y_pred = model.predict(X)
new_pred = list()
for i in range(len(y_pred)):
    new_pred.append(y_pred[i][0])
fl['pred'] = new_pred
fl_bus = fl.groupby('norm_id').agg({'pred':'max','actual':'max'})
fl_bus['real_pred'] = (fl_bus['pred'] >=0.8).astype(int)
acc = accuracy_score(list(fl_bus['real_pred']),list(fl_bus['actual']))

# predict california
X = california[features].values
y_pred = model.predict(X)
new_pred = list()
for i in range(len(y_pred)):
    new_pred.append(y_pred[i][0])
ca['pred'] = new_pred
ca_bus = ca.groupby('norm_id').agg({'pred':'max', 'address':'max', 'name':'max'})
ca_bus = ca_bus.reset_index()

# get file name from txt file and export to that name
file_names = open("file_names.txt", "r")
exp_name = file_names.readlines()[6].strip()

ca_bus.to_csv(exp_name, index=False)
