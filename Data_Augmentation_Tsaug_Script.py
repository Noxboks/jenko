from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
from pandas import read_csv, DataFrame

dataset = read_csv('CLEANED_ECX_EUA_.csv', delimiter=",", engine='python')
dataset.columns=['Date','Open','High','Low','Settle','Change','CloseToPredict']
dataset = dataset.drop(columns=['Date', 'Change', 'CloseToPredict'])

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

new.to_csv("SYNTHETIC_DATA_3K_SAMPLE.csv", index=False, header=False)
