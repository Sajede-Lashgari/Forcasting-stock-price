# -*- coding: utf-8 -*-
"""forcasting_Stock_price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WENklC1_Z61LhXfjumTUoMXSiMnAicSU
"""

#Libraries and settings
import numpy as np
import pandas as pd
import math
import sklearn
import sklearn.preprocessing
import datetime
import os
import tensorflow as tf
from matplotlib import pyplot as plt
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
 
url = '/content/drive/My Drive/اخابر.csv'
data1 = pd.read_csv(url, #index_col=['Date-S']
                    )
data1.head(10)

#descriptive statistics
data1.describe()

#check missing values, show the number of missing values in the dataset.
data1.isnull().sum()

# Sort DataFrame by date
df = data1.sort_values('Date-S')

plt.figure(figsize=(20,10));
plt.plot(df.Open.values, color='red', label='open')
plt.plot(df.Last.values, color='blue', label='last')
plt.plot(df.Close.values, color='green', label='close')
plt.xticks(range(0,df.shape[0],45), df['Date-S'].loc[::45], rotation=45)
plt.title('Historical Stock Price',fontsize=20)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.legend(loc='best')
plt.show()

plt.figure(figsize=(20,10));
plt.plot(df.Lowest.values, color='yellow', label='low')
plt.plot(df.Highest.values, color='black', label='high')
plt.xticks(range(0,df.shape[0],45), df['Date-S'].loc[::45], rotation=45)
plt.title('Historical Stock Price',fontsize=20)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.legend(loc='best')
plt.show()

plt.figure(figsize=(20,10));
plt.plot(df.Volume.values, color='purple', label='volume')
plt.title('Stock volume',fontsize=20)
plt.xticks(range(0,df.shape[0],45), df['Date-S'].loc[::45], rotation=45)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Volume',fontsize=18);

data1.tail()

# Train & Test split
#data2 = pd.read_csv(url, index_col=['Date-S']
#                    )
#data2

data_train = data1.loc[:2285]#2.loc[:'13980325', :]
data_test = data1.loc[2285:]#2.loc['13980326':, :]
data_train.shape

# dimensionality reduction
data_train = data_train['Close']
data_test = data_test['Close']

pd.DataFrame(data_train)

from numpy import array
import numpy as np
# split a univariate sequence into samples
def split_sequence(sequence, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)
 
 # define input sequence
raw_seq = data_train

# choose a number of time steps
n_steps_in, n_steps_out = 60,7 
# split into samples
X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
print(X.shape, y.shape)
X

# Normalize just Close price
x_scaler = MinMaxScaler()
X_train = x_scaler.fit_transform(X)

pd.DataFrame(X_train)
  ######################## dar nahayat ba in kar mikonim az inja bebad

y_scaler = MinMaxScaler()
y_train = y_scaler.fit_transform(y)
y_train
pd.DataFrame(y_train)

# function for min-max normalization of stock
stock = data1.loc[:2285]
sc = MinMaxScaler(feature_range = (0, 1))
set_scaled = sc.fit_transform(stock)
dsc = pd.DataFrame({'Open': set_scaled[:, 0],'Close':set_scaled[:,1],'Highest':set_scaled[:, 2],'Lowest':set_scaled[:,3],'Last':set_scaled[:,4],'Volume':set_scaled[:,5]})
date = stock.iloc[:,0:2]
norm = pd.concat([date, dsc],axis=1)
dd = pd.DataFrame(norm['Close'])
norm

plt.figure(figsize=(20, 10));
plt.plot(norm.Open.values, color='red', label='Open')
plt.plot(norm.Close.values, color='green', label='Close')
plt.plot(norm.Lowest.values, color='blue', label='Lowest')
plt.plot(norm.Highest.values, color='black', label='Highest')
plt.plot(norm.Last.values, color='yellow', label='Last')
plt.title('Normalized price',fontsize=20)
plt.xticks(range(0,data1[:2285].shape[0],45), data1.loc[:2285]['Date-S'].loc[::45], rotation=45)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.legend(loc='best')
plt.show()

plt.figure(figsize=(20, 10));
plt.plot(norm.Volume.values, color='purple', label='Volume')
plt.title('Normalized volume',fontsize=20)
plt.xticks(range(0,data1[:2285].shape[0],45), data1.loc[:2285]['Date-S'].loc[::45], rotation=45)
plt.xlabel('Date',fontsize=18)
plt.ylabel('Volume',fontsize=18)
plt.show()

# baraye shabake

# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], n_features))
print(X_train.shape)
print(y_train.shape)
print(data_train.shape)

# define model
model = Sequential()
model.add(LSTM(80, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
model.add(Dropout(0.2))
model.add(LSTM(80, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse',metrics=['accuracy'])
model.summary()

from keras.utils.vis_utils import plot_model
plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

# fit model
history = model.fit(X_train, y_train, epochs=450, batch_size=64, verbose=2)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()

x_input = X_train
y_predT = model.predict(x_input, verbose=2)
# Visualising the results
y_predT = y_scaler.inverse_transform(y_predT)
print(y_predT)

y_trueT = y_scaler.inverse_transform(y_train)
print(y_trueT)

# Visualising the results
plt.figure(figsize=(20, 10));
plt.plot(y_trueT[:,6], color = 'red', label = 'Real AKHABER Stock Price')
plt.plot(y_predT[:,6], color = 'blue', label = 'Predicted AKHABER Stock Price')
plt.title('Akhaber Stock Price Prediction in Train time',fontsize=20)
plt.ylabel('Close price',fontsize=18)
plt.xticks(range(0,data1[:2285].shape[0],50), data1[:2285]['Date-S'].loc[::50], rotation=45)
plt.xlabel('Date',fontsize=18)
plt.legend()
plt.show()

#data_test = np.array(data_test)

X_test, y_test = [], []

from numpy import array
import numpy as np
# split a univariate sequence into samples
def split_sequence(sequence, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)
 
 # define input sequence
raw_seq = data_test
# choose a number of time steps
n_steps_in, n_steps_out = 60,7 
# split into samples
X_test, y_test = split_sequence(raw_seq, n_steps_in, n_steps_out)
print(X_test.shape, y_test.shape)

X_test, y_test = np.array(X_test), np.array(y_test)
X_test.shape, y_test.shape

x_scalerT = MinMaxScaler()
X_test = x_scalerT.fit_transform(X_test)

y_scalerT = MinMaxScaler()
y_test = y_scalerT.fit_transform(y_test)

pd.DataFrame(X_test)

X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
y_test.shape

# rooye dade Test
x_input = X_test
y_predS = model.predict(x_input)
y_predS = y_scaler.inverse_transform(y_predS)
y_trueS = y_scaler.inverse_transform(y_test)
print(y_predS)
y_trueS

# evaluate network
#run the test dataset
test_error_rate = model.evaluate(X_test, y_test, verbose=0)
print(
      "{} : {:.2f}%".format(model.metrics_names[1],
              test_error_rate[1]*100))
print(
      "{} : {:.2f}%".format(model.metrics_names[0],
              test_error_rate[0]*100))

#run the train dataset
train_error_rate = model.evaluate(X_train, y_train, verbose=2)
print(
      "{} : {:.2f}%".format(model.metrics_names[1],
              train_error_rate[1]*100))
print(
      "{} : {:.2f}%".format(model.metrics_names[0],
              train_error_rate[0]*100))

!sudo pip install h5py

# save network
model.save('Stack_Akhaber.h5')
from keras.models import load_model
# load model from single file
Univariate = load_model('Stack_Akhaber.h5')

# Visualising the results
plt.figure(figsize=(20, 10));
plt.plot(y_trueS[:,6], color = 'red', label = 'Real AKHABER Stock Price')
plt.plot(y_predS[:,6], color = 'blue', label = 'Predicted AKHABER Stock Price')
plt.title('Akhaber Stock Price Prediction in Test time',fontsize=20)
plt.ylabel('Close price',fontsize=18)
plt.xticks(range(0,data1[2285:].shape[0],10), data1[2285:]['Date-S'].loc[::10], rotation=45)
plt.xlabel('Date',fontsize=18)
plt.legend()
plt.show()

print(X_train.shape)
print(y_train.shape)
print(y_predT.shape)
print(data_train.shape)
2286-2220

# demonstrate prediction in 7 days of future
x_input = np.array(data_test[-n_steps_in:]) 
x_input = x_input.reshape((n_steps_in, 1))

scaler = MinMaxScaler()
x_input = scaler.fit_transform(x_input)

x_input = x_input.reshape((1, n_steps_in, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)
yhat = scaler.inverse_transform(yhat)
yhat

############### Final ################ --> model1