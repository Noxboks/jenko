import numpy
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
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
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.layers import Reshape

# Creation of the model
def create_model(optimizer='adam'):
    print("---------- Model creation ----------")

    model = Sequential()
    model.add(Reshape((X.shape[1])))
    model.add(LSTM(128, activation="relu", input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(12, input_dim=5))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam', metrics=['accuracy'])
    return model

# Seed setting to achieve reproducibility
seed = 7
numpy.random.seed(seed)

# Dataset loading
dataset = numpy.loadtxt("EURUSD_15_shifted_Opti.txt", delimiter=",")

# Dataset split to train and test
X = dataset[:,0:5]
Y = dataset[:,5]

X = X.reshape((X.shape[0], X.shape[1]))
Y = Y.reshape((Y.shape[0], Y.shape[1]))

# Wrapping of the model to the Keras classifier
model = KerasClassifier(build_fn=create_model, epochs=10, batch_size=128, verbose=0)

# Declaration of optimizers and GridSearch
optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
param_grid = dict(optimizer=optimizer)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, cv=3)
grid_result = grid.fit(X, Y)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

#OUTPUT: Best: 0.700521 using {'optimizer': 'RMSprop'}
