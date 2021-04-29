import numpy
from keras.layers import Dropout
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM
from keras.layers import Flatten, Concatenate
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
import joblib
from keras import backend as K
from keras.layers import Activation
import sherpa

def custom_activation(x, beta=1):
    return (K.sigmoid(beta * x) * x)

dataset = read_csv("ECX_EUA_DATASET_CLEAN.csv", delimiter=",")

print("------------------ Dataset Reading ------------------")

# Scale the data from 0 to 1
dataset = dataset.subtract(dataset.mean())
values = dataset.values
scaler = MinMaxScaler(feature_range=(0, 1))
values = scaler.fit_transform(values)
joblib.dump(scaler, 'Provisional_Stacking_Ensemble_X.pkl')

print("----------------- Dataset Spliting -----------------")
n_train_hours = int(len(dataset)*0.8)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]

train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

print("----------------- Dataset Shaping ------------------")
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))


model1 = Sequential()
model1.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(1, 4)))
model1.add(Activation(custom_activation, name="Swish"))
model1.add(Dropout(0.2))
model1.add(LSTM(units=50, return_sequences=True))
model1.add(Activation(custom_activation))
model1.add(Dropout(0.2))
model1.add(LSTM(units=50))
model1.add(Activation(custom_activation))
model1.add(Dropout(0.2))
model1.add(Dense(units=1, activation='relu'))
model1.add(Dense(1))

model2 = Sequential()
model2.add(Conv1D(filters=64, kernel_size=1, activation='relu', input_shape=(1, 4)))
model2.add(MaxPooling1D(pool_size=1))
model2.add(Flatten())
model2.add(Dense(50))
model2.add(Dense(1))

merged = Concatenate()([model1.output, model2.output])
z = Dense(128)(merged)
z = Dropout(0.25)(z)
z = Dense(10)(z)
z = Dense(1)(z)

model = Model(inputs=[model1.input, model2.input], outputs=z)


print("---------------- Model Compilation -----------------")
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error',
                                                                     'mean_absolute_error',
                                                                     'mean_absolute_percentage_error',
                                                                     'cosine_proximity', 'accuracy'])

# parameters = [sherpa.Discrete('num_units', [50, 200])]
batches = numpy.arange(25, 1001, 25).tolist()
dropouts = numpy.arange(0.001, 1.001, 0.002).tolist()
learning_rates = numpy.arange(0.0001, 1.0001, 0.0001).tolist()
activations = ['relu', 'elu', 'prelu', 'Adadelta', 'Adagrad', 'Adam', 'Adamax', 'Ftrl', 'Nadam', 'RMSprop', 'SGD']

parameters = [sherpa.Continuous(name='lr', range=learning_rates, scale='log'),
              sherpa.Ordinal(name='batch_size', range=batches),
              sherpa.Choice(name='activation', range=activations)]

# alg = sherpa.algorithms.RandomSearch(max_num_trials=50)
alg = sherpa.algorithms.GPyOpt(max_num_trials=150)
study = sherpa.Study(parameters=parameters,
                     algorithm=alg,
                     lower_is_better=True)

for trial in study:
    model1 = Sequential()
    model1.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(1, 4)))
    model1.add(Activation(custom_activation, name="Swish"))
    model1.add(Dropout(0.2))
    model1.add(LSTM(units=50, return_sequences=True))
    model1.add(Activation(custom_activation))
    model1.add(Dropout(0.2))
    model1.add(LSTM(units=50))
    model1.add(Activation(custom_activation))
    model1.add(Dropout(0.2))
    model1.add(Dense(units=1, activation='relu'))
    model1.add(Dense(1))

    model2 = Sequential()
    model2.add(Conv1D(filters=64, kernel_size=1, activation='relu', input_shape=(1, 4)))
    model2.add(MaxPooling1D(pool_size=1))
    model2.add(Flatten())
    model2.add(Dense(50))
    model2.add(Dense(1))

    merged = Concatenate()([model1.output, model2.output])
    z = Dense(128)(merged)
    z = Dropout(0.25)(z)
    z = Dense(10)(z)
    z = Dense(1)(z)

    model = Model(inputs=[model1.input, model2.input], outputs=z)

    print("---------------- Model Compilation -----------------")
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error',
                                                                        'mean_absolute_error',
                                                                        'mean_absolute_percentage_error',
                                                                        'cosine_proximity', 'accuracy'])
    history = model.fit([train_X, train_X], train_y, epochs=50, batch_size=512, validation_data=([test_X,test_X], test_y),
                        callbacks=[study.keras_callback(trial, objective_name='val_loss')], verbose=2)

    study.finalize(trial)

print(study.get_best_result())