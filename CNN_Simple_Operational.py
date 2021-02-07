from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
import keras
from scipy.stats import wasserstein_distance
import joblib


class CustomSaver(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        self.model.save("model_CNN_{}".format(epoch))


dataset = read_csv('TEST_25_01_2020_OIL_GAS_WITH_EUA.csv', delimiter=",", engine='python')
dataset = dataset.drop_duplicates()
values = dataset.values

n_steps = len(dataset.columns)-1

scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)

# --------

n_train_hours = int(len(dataset)*0.8)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]


X, y = train[:, :-1], train[:, -1]
X_test, y_test = test[:, :-1], test[:, -1]

# --------

# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

saver = CustomSaver()

# define model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))

joblib.dump(scaler, 'Scaler.pkl')

model.compile(optimizer='Adam', loss='mae')
# fit model
history = model.fit(X, y, callbacks=[saver], epochs=500, batch_size=64, validation_data=(X_test, y_test), verbose=2)

pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

# Prediction

yhat = model.predict(X_test)
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1]))

inv_yhat = concatenate((yhat, X_test[:, :]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:, 0]

y_test = y_test.reshape((len(y_test), 1))
inv_y = concatenate((y_test, X_test[:, :]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:, 0]

print(inv_y)

pyplot.plot(inv_yhat)
pyplot.plot(inv_y)
pyplot.legend(['Forecast', 'Actual Values'])
pyplot.show()

rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.10f' % rmse)
print(str(history.history['val_loss'][-1]))
print("")
print("DISTANCE: ", wasserstein_distance(inv_yhat, inv_y))
