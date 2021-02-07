import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse

warnings.filterwarnings("ignore")

# Data import
dataset = pd.read_csv('EURUSD_1MTF_TEST_V2.csv', delimiter=",", engine='python', nrows=10000)
dataset.columns = ['Open', 'High', 'Low', 'Close', 'ClosePredict']
dataset = dataset.drop(columns=['Open', 'High', 'Low', 'ClosePredict'])

# Data split
n_train_hours = int(len(dataset) * 0.8)
train = dataset.iloc[:n_train_hours, :]
test = dataset.iloc[n_train_hours:, :]

# Model definition
model = SARIMAX(train['Close'], order=(1, 1, 2), seasonal_order=(2, 1, 2, 12))

# Model fitting
result = model.fit()
result.summary()

start = len(train)
end = len(train) + 100

# Model prediction
predictions = result.predict(start, end, typ='levels').rename("Predictions")

# Result visualisation
predictions.plot(legend=True)
test['Close'].plot(legend=True)

# Model evaluation
rmse(test['Close'], predictions)
mean_squared_error(test['Close'], predictions)
