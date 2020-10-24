# univariate lstm example
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from pandas import read_csv
from pandas import DataFrame
import numpy

from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
import pandas
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, BatchNormalization
from keras import optimizers
import keras
from keras.utils.generic_utils import get_custom_objects
from keras import backend as K
from keras.layers import Activation

from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D, Conv2D
from keras.layers.convolutional import MaxPooling1D
 
# split a univariate sequence into samples
def split_sequence(sequence, n_steps):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the sequence
		if end_ix > len(sequence)-1:
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
		X.append(seq_x)
		y.append(seq_y)
		#print("X: ", array(X))
		#print("Y: ", array(y))
	return array(X), array(y)

def create_sequences(dataset, shifting):
    complete_list_X = []
    complete_list_y = []

    values = dataset.values
    scaler = MinMaxScaler(feature_range=(0, 1))
    values = scaler.fit_transform(values)

    # X = array(values[:n_train_hours, 0:30])
    # y = array(values[:n_train_hours,30])

    # X_test = array(values[n_train_hours:, 0:30])
    # y_test = array(values[n_train_hours:,30])

    for l in range(len(dataset)-shifting):
        a = array(values[l:l+shifting, :,])
        b = array(values[l+shifting:l+shifting+1,-1])[0]
        complete_list_y.append(b)

        full = []
        
        for i in range(len(a)):
            for k in range(len(a[i])):
                full.append(a[i][k])

        complete_list_X.append(full)

    return array(complete_list_X), array(complete_list_y)
 
# define input sequence
raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# choose a number of time steps
n_steps = 30
# split into samples

# X, y = split_sequence(raw_seq, n_steps)

dataset = read_csv('Berger-2019-janv2020-total - Clean - Final.csv', delimiter=",", engine='python')

# test_seq_x, test_seq_y = create_sequences(dataset, 3)

complete_list_X = []
complete_list_y = []

shifting = 5

# values = dataset.values
# scaler = MinMaxScaler(feature_range=(0, 1))
# values = scaler.fit_transform(values)

# X = array(values[:n_train_hours, 0:30])
# y = array(values[:n_train_hours,30])

# X_test = array(values[n_train_hours:, 0:30])
# y_test = array(values[n_train_hours:,30])

# SAVE print(array(dataset.iloc[:, 0:30]))
# SAVE print("y: ", dataset.iloc[:,30])

n_train_hours = 16515

# values = dataset.values
# scaler = MinMaxScaler(feature_range=(0, 1))
# values = scaler.fit_transform(values)

# X = array(values[:n_train_hours, 0:30])
# y = array(values[:n_train_hours,30])

# X_test = array(values[n_train_hours:, 0:30])
# y_test = array(values[n_train_hours:,30])

# --------

X = array(dataset.iloc[:n_train_hours, 0:30])
y = array(dataset.iloc[:n_train_hours,30])

X_test = array(dataset.iloc[n_train_hours:, 0:30])
y_test = array(dataset.iloc[n_train_hours:,30])

# --------

print(len(y))
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

# define model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='Adam', loss='mae')
# fit model
history = model.fit(X, y, epochs=200, batch_size=16, validation_data=(X_test, y_test), verbose=2)

pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# Prediction

yhat = model.predict(X_test)
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1]))
#X_test = X_test.reshape((1, 30, 1))

inv_yhat = concatenate((yhat, X_test[:, -30:]), axis=1)
# inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

y_test = y_test.reshape((len(y_test), 1))
inv_y = concatenate((y_test, X_test[:, -30:]), axis=1)
# inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

print(inv_y)

pyplot.plot(inv_yhat)
pyplot.plot(inv_y)

pyplot.show()

rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.10f' % rmse)
print(str(history.history['val_loss'][-1]))
