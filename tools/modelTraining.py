import pandas as pd
import pickle

# 讀取資料集
def training(df,filename='document/aa5.csv',savePath="static/model/"):
    #if(df):
     #   df = pd.read_csv(filename)
    #print(df)

    # 顯示資料集的描述資料
    print('資料集的描述：')
    print(df.describe())

    # 顯示沒有資料的筆數
    print('沒有資料的筆數：')
    print(df.isnull().sum())
    try:
        decisionTree(df,savePath)
        randomForest(df,savePath)
        logisticregression(df,savePath)
        supportVectorMachine(df,savePath)
        neuralNetwork(df,savePath)
    except Exception as e:
        print(e.with_traceback())
        return False
    return True


def decisionTree(df,savePath):  # Decision tree
    # 資料處理1 Decision tree
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler

    clf = DecisionTreeClassifier(
        criterion='entropy', max_depth=5, min_samples_leaf=9)
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]

    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()

    # Divide by class
    X_train_class_0 = X_train[Y_train == 0]
    X_train_class_1 = X_train[Y_train == 1]
    X_train_class_0_under = X_train_class_0.sample(
        X_train_class_1.shape[0])  # 174
    X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    X_train_final = X_train_under
    Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    print('X_train_final.shape：{}'.format(X_train_final.shape))
    print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型1 Decision tree
    print("Training ...")
    clf.fit(X_train_final, Y_train_final)

    # 評估模型1 Decision tree
    print("Testing ...")
    # 計算訓練資料集的準確度
    accuracy = clf.score(X_train_final, Y_train_final)
    print("Decision tree 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'NF_decisionTree.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(clf, f)


def randomForest(df,savePath):  # Random forest
    # 資料處理2 Random forest
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    rf = RandomForestClassifier(
        n_estimators=750, max_depth=20, criterion='entropy', max_features='sqrt')
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]

    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()

    # Divide by class
    X_train_class_0 = X_train[Y_train == 0]
    X_train_class_1 = X_train[Y_train == 1]
    X_train_class_0_under = X_train_class_0.sample(
        X_train_class_1.shape[0])  # 174
    X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    X_train_final = X_train_under
    Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    print('X_train_final.shape：{}'.format(X_train_final.shape))
    print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型2 Random forest
    print("Training ...")
    rf.fit(X_train_final, Y_train_final)

    # 評估模型2 Random forest
    print("Testing ...")
    # 計算訓練資料集的準確度
    accuracy = rf.score(X_train_final, Y_train_final)
    print("Random forest 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'NF_randomForest.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(rf, f)


def logisticregression(df,savePath):  # Logistic Regression
    # 資料處理3 Logistic Regression
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    logreg = LogisticRegression(penalty='l2', C=0.01)
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]

    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()

    # Divide by class
    X_train_class_0 = X_train[Y_train == 0]
    X_train_class_1 = X_train[Y_train == 1]
    X_train_class_0_under = X_train_class_0.sample(
        X_train_class_1.shape[0])  # 174
    X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    X_train_final = X_train_under
    Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    print('X_train_final.shape：{}'.format(X_train_final.shape))
    print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型3 Logistic Regression
    print("Training ...")
    logreg.fit(X_train_final, Y_train_final)

    # 評估模型3 Logistic Regression
    print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = logreg.score(X_train_final, Y_train_final)
    print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'NF_logisticregression.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(logreg, f)


def supportVectorMachine(df,savePath):  # Support Vector Machine
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler

    model = SVC(kernel='rbf', C=10, gamma=0.0001, cache_size=1000,probability=True)
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]

    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()

    # Divide by class
    print("Data Rescaling ...")
    X_train_class_0 = X_train[Y_train == 0]
    X_train_class_1 = X_train[Y_train == 1]
    X_train_class_0_under = X_train_class_0.sample(
        X_train_class_1.shape[0])  # 174
    X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    X_train_final = X_train_under
    Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    print('X_train_final.shape：{}'.format(X_train_final.shape))
    print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型5 Support Vector Machine
    print("Training ...")
    model.fit(X_train_final, Y_train_final)

    # 評估模型5 Support Vector Machine
    print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = model.score(X_train_final, Y_train_final)
    print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'NF_supportVectorMachine.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(model, f)
def neuralNetwork(df,savePath):
    
    
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
    
    print("Saving Model: ...")
    model_file_name = 'NF_neuralNetwork.pickle'
    model.save(savePath+'NF_neuralNetwork.h5')
if __name__=="__main__":
    df = pd.read_csv("document/aa5.csv")
    training(df)
# decisionTree()
# randomForest()
# logisticregression()
# supportVectorMachine()
