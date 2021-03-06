from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
import pandas
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM

# Convert the dataset to a supervised dataset
def series_to_supervised(data, n_in=0, n_out=0, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    dframe = DataFrame(data)
    cols, names = list(), list()

    for i in range(n_in, 0, -1):
        cols.append(dframe.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

    for i in range(0, n_out):
        cols.append(dframe.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('vars%d(t+%d)' % (j+1)) for j in range(n_vars)]

    mer = concat(cols, axis=1)
    mer.columns = names

    if dropnan:
        mer.dropna(inplace=True)

    return mer

# Read data of file 
dataset = read_csv('Solar_Processed.csv', engine='python')
del dataset["Time"]
values = dataset.values
groups = [0, 1, 2, 3, 4, 5]
i = 1

# Scale the data from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

# Create supervised dataset with the scaled data and drop unscaled ones
reframed = series_to_supervised(scaled, 1, 1)
pandas.set_option('display.max_columns', 100)
reframed.drop(reframed.columns[[7, 8, 9,10,11]], axis=1, inplace=True)
values = reframed.values

# Split the values in two groups train and test
# Modify the shape of the arrays to feed the model
n_train_hours = 365*24
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

# Model specification
model = Sequential([
    LSTM(128, input_shape=(train_X.shape[1], train_X.shape[2]), activation='relu'),
    Dense(10),
    Dense(1),
])

# Model compilation
model.compile(optimizer='adam', loss='mae')

history = model.fit(train_X, train_y, epochs=100, batch_size=128, validation_data=(test_X, test_y), verbose=2)

# Set the visualisation of the model output
# Modify the values to their original form to populate the graphs
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))

inv_yhat = concatenate((yhat, test_X[:, -5:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]

test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -5:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

print(inv_y)

pyplot.plot(inv_yhat)
pyplot.plot(inv_y)

pyplot.show()

rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)
