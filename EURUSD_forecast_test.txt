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

print("script_python_v2.8")

# Convert the dataset to a supervised dataset
def series_to_supervised(data, n_in=0, n_out=0, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)

    cols, names = list(), list()

    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('vars%d(t+%d)' % (j+1)) for j in range(n_vars)]

    agg = concat(cols, axis=1)
    agg.columns = names

    if dropnan:
        agg.dropna(inplace=True)

    #print(df)

    return agg

# Read data of file 
dataset = read_csv('EURUSD-M1.csv', delimiter=",", encoding='utf_16', engine='python')


values = dataset.values
groups = [0, 1, 2, 3, 4, 5, 6, 7]
i = 1

print("------------------ Dataset Reading ------------------")

# Scale the data from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)
#print(values)
# Create supervised dataset with the scaled data and drop unscaled ones
#reframed = series_to_supervised(values, 1, 1)
pandas.set_option('display.max_columns', 100)
#reframed.drop(reframed.columns[[5, 6, 7, 8, 9]], axis=1, inplace=True)
#values = reframed.values

# Split the values in two groups train and test
# Modify the shape of the arrays to feed the model
n_train_hours = 1485335
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

print("----------------- Dataset Spliting -----------------")

train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print("----------------- Dataset Shaping ------------------")
# Model specification 0.0032
model = Sequential()
#model.add(LSTM(64, input_shape=(train_X.shape[1], train_X.shape[2]), return_sequences=True))
#model.add(Activation('relu'))
#model.add(Dropout(0.5))
#model.add(BatchNormalization())
#model.add(LSTM(64))
#model.add(Activation('relu'))
#model.add(Dropout(0.5))
#model.add(BatchNormalization())
#model.add(LSTM(64))
#model.add(Activation('relu'))
#model.add(Dropout(0.5))
#model.add(BatchNormalization())
#model.add(Dense(10))
#model.add(Activation('relu'))
#model.add(Dropout(0.5))
#model.add(BatchNormalization())
#model.add(Dense(1))

model.add(LSTM(64, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Dense(1))

print("----------------- Model Definition -----------------")
# Model compilation
model.compile(optimizer='Adam', loss='mae')

print("---------------- Model Compilation -----------------") #len(train_X)

history = model.fit(train_X, train_y, epochs=10, batch_size=128, validation_data=(test_X, test_y), verbose=2)

# Set the visualisation of the model output
# Modify the values to their original form to populate the graphs
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

inv_yhat = concatenate((yhat, test_X[:, -10:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -10:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

print(inv_y)

pyplot.plot(inv_yhat)
pyplot.plot(inv_y)

pyplot.show()

rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.10f' % rmse)
print(str(history.history['val_loss'][-1]))
model.save("script_python_v2.8-"+str(history.history['val_loss'][-1])+".h5")
