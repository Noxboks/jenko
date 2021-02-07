import numpy as np
from tsaug.visualization import plot
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
from pandas import read_csv, DataFrame
from matplotlib import pyplot

dataset = read_csv('CLEANED_ECX_EUA_Future_DT_2008_to_2021.csv', delimiter=",", engine='python')
dataset.columns=['Date','Open','High','Low','Settle','Change','CloseToPredict']
dataset = dataset.drop(columns=['Date', 'Change', 'CloseToPredict'])

# X = np.load('CLEANED_ECX_EUA_Future_DT_2008_to_2021.csv', allow_pickle=True)

X = dataset.to_numpy()
X = X.reshape(len(dataset.columns), len(dataset))
print(len(X))

print(X.shape)
my_augmenter = (
    TimeWarp() * 1
    + Crop(size=3000)
    + Quantize(n_levels=[10, 20, 30])
    + Drift(max_drift=(0.1, 0.5)) @ 0.8
    + Reverse() @ 0.5
)


X_aug = my_augmenter.augment(X)
print(X)
print(X_aug)

test = X_aug.reshape(-1, 4)
new = DataFrame(test)
print(new)

new.to_csv("SYNTHETIC_DATA_SAMPLE_3K_10.csv", index=False, header=False)
