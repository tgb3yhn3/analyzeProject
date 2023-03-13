import pandas as pd
import pickle

# 讀取資料集
df = pd.read_csv('tools/document/aa5.csv')
print(df)

# 顯示資料集的描述資料
print('資料集的描述：')
print(df.describe())

# 顯示沒有資料的筆數
print('沒有資料的筆數：')
print(df.isnull().sum())


def decisionTree():  # Decision tree
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
    model_file_name = 'model/decisionTree.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(clf, f)


def randomForest():  # Random forest
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
    model_file_name = 'model/randomForest.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(rf, f)


def logisticregression():  # Logistic Regression
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
    model_file_name = 'model/logisticregression.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(logreg, f)


def supportVectorMachine():  # Support Vector Machine
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler

    model = SVC(kernel='rbf', C=10, gamma=0.0001, cache_size=1000)
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
    model_file_name = 'model/supportVectorMachine.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(model, f)


# decisionTree()
# randomForest()
# logisticregression()
# supportVectorMachine()
