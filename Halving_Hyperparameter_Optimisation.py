import numpy
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import GridSearchCV, HalvingGridSearchCV, HalvingRandomSearchCV
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten
from keras.wrappers.scikit_learn import KerasClassifier
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from numpy import genfromtxt


# Creation of the model
def create_model(optimizer='Adam', n_steps=4, n_features=1):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss='mae', metrics=['accuracy'])
    return model

# Seed setting to achieve reproducibility
seed = 7
numpy.random.seed(seed)

# Dataset loading
dataset = read_csv('EURUSD_1MTF_TEST_V2.csv', delimiter=",", engine='python')
values = dataset.values
scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)

# --------

n_train_hours = int(len(dataset)*0.8)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]


X, y = train[:, :-1], train[:, -1]
X_test, y_test = test[:, :-1], test[:, -1]

# --------

print(len(y))
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))
# -----

# Wrapping of the model to the Keras classifier
model = KerasClassifier(build_fn=create_model, epochs=200, batch_size=60, verbose=2)

# Declaration of batch size, training epochs and GridSearch
batch_size = [10, 20, 40, 60, 80, 100]
epochs = [10, 50, 100, 200, 500]
optimizers = ['Adadelta', 'Adagrad']
param_grid = dict(optimizer=optimizers, batch_size=batch_size, epochs=epochs)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1) # n_jobs = -1 to run search in parallel
# grid = HalvingRandomSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3) # n_jobs = -1 to run search in parallel
grid_result = grid.fit(X, y)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))