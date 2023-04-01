import pandas as pd
df = pd.read_csv('aa5.csv')
import numpy as np
dataset = df.values
np.random.shuffle(dataset)
dataset = pd.DataFrame(dataset)
X = dataset.iloc[:, :5]
y = dataset.iloc[:, 5]
# 定義模型
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler


X_train_class_0 = X[y == 0]
X_train_class_1 = X[y == 1]
X_train_class_0_under = X_train_class_0.sample(X_train_class_1.shape[0])
X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
X_train = X_train_under
y_train = y[X_train_under.index]
X_train_mean = X_train.mean(axis=0)
X_train_std = X_train.std(axis=0)
print(X_train_mean)
print(X_train_std)

#正規化
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train))

# 定義模型
model = Sequential()
model.add(Dense(28, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.75))
model.add(Dense(1,  activation='sigmoid'))

# 顯示模型摘要資訊
print('模型摘要資訊：')
model.summary()


# 編譯模型
model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])

# 訓練模型
print("Training ...")
# X_train：訓練資料的特徵資料
# Y_train：訓練資料的輸出欄位
# validation_split：分割出驗證資料集的比例
# epochs：訓練週期
# batch_size：批次大小
# verbose：訓練過程中訊息顯示的詳細程度
model.fit(X_train, y_train, epochs=300)

print("Testing ...")

# 計算訓練資料集的準確度
accuracy = model.evaluate(X_train, y_train)
print(accuracy)
X = df.iloc[:, :5]
Y = df.iloc[:, 5]

X = pd.DataFrame(scaler.fit_transform(X))
accuracy = model.evaluate(X, Y)
print(accuracy)
import pickle
print("Saving Model: ...")
model_file_name = 'NF_neuralNetwork.pickle'
model.save('my_model.h5')
# with open(model_file_name, 'wb') as f:
#     pickle.dump(model, f)