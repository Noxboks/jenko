import numpy
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

# Creation of the model
def create_model():
    model = Sequential()
    model.add(Dense(12, input_dim=5, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Seed setting to achieve reproducibility
seed = 7
numpy.random.seed(seed)

# Dataset loading
dataset = numpy.loadtxt("EURUSD_15_shifted_Opti.txt", delimiter=",")

# Dataset split to train and test
X = dataset[:,0:5]
Y = dataset[:,5]

# Wrapping of the model to the Keras classifier
model = KerasClassifier(build_fn=create_model, verbose=0)

# Declaration of batch size, training epochs and GridSearch
batch_size = [10, 20, 40, 60, 80, 100]
epochs = [10, 50, 100]
param_grid = dict(batch_size=batch_size, epochs= epochs)
grid = GridSearchCV(estimator= model, param_grid=param_grid, n_jobs=1, cv=3)
grid_result = grid.fit(X, Y)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))




