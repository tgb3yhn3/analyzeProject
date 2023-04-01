import pickle
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np
model = load_model('my_model.h5')
df = pd.read_csv('aa5.csv')
X_train = df.iloc[:, :5]
Y_train = df.iloc[:, 5]
X_train_class_0 = X_train[Y_train == 0]
X_train_class_1 = X_train[Y_train == 1]
X_train_class_0_under = X_train_class_0.sample(X_train_class_1.shape[0])
X_train_mean = X_train_class_0_under.mean(axis=0)
X_train_std = X_train_class_0_under.std(axis=0)
sea_transform = (0 - X_train_mean.sea) / X_train_std.sea
wbc_transform = (14800 - X_train_mean.wbc) / X_train_std.wbc
crp_transform = (34.84 - X_train_mean.crp) / X_train_std.crp
seg_transform = (84.1 - X_train_mean.seg) / X_train_std.seg
band_transform = (0 - X_train_mean.band) / X_train_std.band
pred = {}
model_file_name = 'neuralNetwork.pickle'
# with open(model_file_name, 'rb') as f:
#     model4 = pickle.load(f)
pred4 = model.predict(np.array(
        [[sea_transform, wbc_transform, crp_transform, seg_transform, band_transform]]))
pred4 = pred4[0][0]
print(pred4)
if (pred4 > 0.5):
  pred['neuralNetwork'] = 1
  pred['neuralNetwork_proba'] = np.round(pred4*100, 2)
else:
  pred['neuralNetwork'] = 0
  pred['neuralNetwork_proba'] = 100 - np.round(pred4*100, 2)
print(pred['neuralNetwork'], pred['neuralNetwork_proba'])