from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
import pandas
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras
from keras.utils.generic_utils import get_custom_objects
from keras import backend as K
from keras.layers import Activation
import joblib

class CustomSaver(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        self.model.save("model_1M_{}".format(epoch))

def custom_activation(x, beta=1):
    return (K.sigmoid(beta * x) * x)



get_custom_objects().update({'custom_activation': Activation(custom_activation)})


# Read data of file
dataset = read_csv('EURUSD_1MTF_TEST_V2.csv', delimiter=",", engine='python')
values = dataset.values


print("------------------ Dataset Reading ------------------")

# Scale the data from 0 to 1
scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)
joblib.dump(scaler, 'Scaler.pkl')

# Split the values in two groups train and test
# Modify the shape of the arrays to feed the model
n_train_hours = int(len(dataset)*0.8)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

print("----------------- Dataset Spliting -----------------")

train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print("----------------- Dataset Shaping ------------------")
# Model specification
model = Sequential()
model.add(LSTM(32, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Activation(custom_activation, name="Swish"))
model.add(Dense(10))
model.add(Activation(custom_activation, name="Swish"))
model.add(Dense(1))
print("----------------- Model Definition -----------------")

# Model compilation
model.compile(optimizer='Adam', loss='mae')

print("---------------- Model Compilation -----------------")  # len(train_X)
saver = CustomSaver()
history = model.fit(train_X, train_y, epochs=50, batch_size=512, validation_data=(test_X, test_y), verbose=2)

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
inv_yhat = inv_yhat[:, 0]

test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, -10:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:, 0]

print(inv_y)

pyplot.plot(inv_yhat)
pyplot.plot(inv_y)

pyplot.show()

comp = pandas.DataFrame(inv_yhat, inv_y)
comp = pandas.DataFrame({'close': inv_y, 'predict': inv_yhat})
comp = comp.head(1000)


rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.10f' % rmse)

print(str(history.history['val_loss'][-1]))
comp.to_csv('output_prediction_eurusd_FULL.csv', header=False)
model.save("script_python_Test-" + str(history.history['val_loss'][-1]))
