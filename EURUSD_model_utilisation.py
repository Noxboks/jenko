from keras.models import load_model
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
import numpy
import joblib
from keras.utils.generic_utils import get_custom_objects
from keras import backend as K
from keras.layers import Activation
    
def custom_activation(x, beta = 1):
    return (K.sigmoid(beta * x) * x)

def preprocessing(lst, scaler):
    data = numpy.array([lst]).T
    values = scaler.fit_transform(data)
    val = values.reshape(1, 1, 7)
    print(val)
    return val

def prediction_postprocessing(val, model):
    modelPredict = model.predict(val)
    print("FIRST PREDICTION: ", modelPredict)
    modelPredict = modelPredict.reshape(1, -1) 
    prediction = scaler.inverse_transform(modelPredict)
    print("PREDICTION: ", prediction)
    return prediction
    
#1.09949,1.09949,1.09925,1.09925,0.0,45.0,5.0

print("---------------------- Custom Activation ----------------------")
get_custom_objects().update({'custom_activation': Activation(custom_activation)})

print("--------------------- Model Loading Start ---------------------")

print("---------------------- Model 5_M Loaded ----------------------")
model_5M = load_model('script_python_v2.8-0.0007653633976586066_5M.h5')

scaler = joblib.load('test_model.pkl')
print("------------------------ Scaler Loaded ------------------------")

print("------------------------ Preprocessing ------------------------")
preprocess_data = preprocessing([1.09946,1.09955,1.09942,1.09946,0.0,6.0,44.0], scaler)
#70
print("------------------------- Predictions -------------------------")
prediction_postprocessing(preprocess_data, model_5M)

print("------------------------- Program End -------------------------")
