import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import auc, confusion_matrix, matthews_corrcoef, roc_curve
#效能相關
acc = []
mcc = []
auroc = []
sen = []
spe = []
testData=[[
    1,12000,240,80,8
]]
target=['sea','wbc','crp','seg','band']
def getItemInOrder(df):
    newData=pd.DataFrame()
    #get column name
    # print(df.head(0))
    headers=list(df.head(0))
    for i in range(len(target)):
        for j in range(len(headers)):
            if target[i] == headers[j]:
                newData[target[i]]=df[target[i]]
    return newData
def dropNotInTarget(df,isneu=False):
    
    if(isneu):
        ans=[]
    else:
        ans=['nf']
    column_headers = list(df.columns)
    for i in range(len(column_headers)):
        #print(column_headers[i])
        if column_headers[i] not in target and column_headers[i] not in ans:
            df=df.drop(column_headers[i],axis=1)
    return df
def decisionTree(df,savePath):  # Decision tree
    # 資料處理1 Decision tree
    df=dropNotInTarget(df)
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler
    
    clf = DecisionTreeClassifier(
        criterion='entropy', max_depth=5, min_samples_leaf=9,random_state=42)
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]
    X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()
    X_train_final=X_train
    Y_train_final=Y_train
    # Divide by class
    # X_train_class_0 = X_train[Y_train == 0]
    # X_train_class_1 = X_train[Y_train == 1]
    # X_train_class_0_under = X_train_class_0.sample(
    #     X_train_class_1.shape[0])  # 174
    # X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    # X_train_final = X_train_under
    # Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    #print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    test_X = pd.DataFrame(scaler.fit_transform(test_X))
    #print('X_train_final.shape：{}'.format(X_train_final.shape))
    #print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型1 Decision tree
    #print("Training ...")
    clf.fit(X_train_final, Y_train_final)

    # 評估模型1 Decision tree
    #print("Testing ...")
    # 計算訓練資料集的準確度
    accuracy = clf.score(test_X, test_y)
    print("Decision tree 訓練資料集的準確度 = {:.4f}".format(accuracy))
    # print(clf.predict(scaler.transform(testData)))
    # print(clf.predict_proba(scaler.transform(testData)))
    # 儲存模型
    model_file_name = savePath+'NF_decisionTree.pickle'
    #return clf
    with open(model_file_name, 'wb') as f:
        pickle.dump(clf, f)
    acc.append(accuracy)
    y_pred = clf.predict(X_train_final)
    mcc.append(matthews_corrcoef(Y_train_final, y_pred))
    fpr, tpr, thresholds = roc_curve(Y_train_final, clf.predict_proba(X_train_final)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(Y_train_final, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}
    
def randomForest(df,savePath):  # Random forest
    # 資料處理2 Random forest
    df=dropNotInTarget(df)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    rf = RandomForestClassifier(
        n_estimators=100, max_depth=7, criterion='entropy', max_features='sqrt')
    scaler = StandardScaler()
    
    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]
    X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()
    X_train_final=X_train
    Y_train_final=Y_train
    # Divide by class
    # X_train_class_0 = X_train[Y_train == 0]
    # X_train_class_1 = X_train[Y_train == 1]
    # X_train_class_0_under = X_train_class_0.sample(
    #     X_train_class_1.shape[0])  # 174
    # X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    # X_train_final = X_train_under
    # Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    # print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    test_X = pd.DataFrame(scaler.fit_transform(test_X))
    # print('X_train_final.shape：{}'.format(X_train_final.shape))
    # print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型2 Random forest
    # print("Training ...")
    rf.fit(X_train_final, Y_train_final)

    # 評估模型2 Random forest
    # print("Testing ...")
    # 計算訓練資料集的準確度
    accuracy = rf.score(test_X, test_y)
    print("Random forest 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # print(rf.predict(scaler.transform(testData)))
    # print(rf.predict_proba(scaler.transform(testData)))
    # 儲存模型
    model_file_name = savePath+'NF_randomForest.pickle'
    #return rf
    imf=rf.feature_importances_
    # print(imf)
    with open(model_file_name, 'wb') as f:
        pickle.dump(rf, f)
    acc.append(accuracy)
    y_pred = rf.predict(X_train_final)
    mcc.append(matthews_corrcoef(Y_train_final, y_pred))
    fpr, tpr, thresholds = roc_curve(Y_train_final, rf.predict_proba(X_train_final)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(Y_train_final, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}



def logisticregression(df,savePath):  # Logistic Regression
    # 資料處理3 Logistic Regression
    df=dropNotInTarget(df)
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    
    # read column header
    # target=['sea','wbc','crp','seg','band']
    # ans=['nf']
    # column_headers = list(df.columns)
    # X_train=[]
    # for i in range(len(column_headers)):
    #     #print(column_headers[i])
    #     if column_headers[i] in target:
    #         X_train.append(df.iloc[:, i])
    #     elif column_headers[i] in ans:
    #         Y_train=df.iloc[:, i]
    # X_train=np.array(X_train).T
    # Y_train=np.array(Y_train).T
    # print(X_train.shape)
    # print(Y_train.shape)
    X_train = df.iloc[:, :5]
    # print(X_train)
    Y_train = df.iloc[:, 5]
    # print(Y_train)
    X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    logreg = LogisticRegression()
    scaler = StandardScaler()

    # 編碼後的X與Y
    # X_train = df.iloc[:, :5]
    # Y_train = df.iloc[:, 5]

    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()

    # Divide by class
    # X_train_class_0 = X_train[Y_train == 0]
    # X_train_class_1 = X_train[Y_train == 1]
    # X_train_class_0_under = X_train_class_0.sample(
    #     X_train_class_1.shape[0])  # 174
    # X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    # X_train_final = X_train_under
    # Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    #print("Data Rescaling ...")
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train))
    test_X=pd.DataFrame(scaler.transform(test_X))
    # print('X_train_final.shape：{}'.format(X_train_final.shape))
    # print('Y_train_final.shape：{}'.format(Y_train_final.shape))
    # Y_train_final = pd.DataFrame(Y_train)
    #print(X_train_final)
    # 訓練模型3 Logistic Regression
    #print("Training ...")
    logreg.fit(X_train_final.values, Y_train.values)

    
    #model_file_name = 'static/model/NF_logisticregression.pickle'
    #with open(model_file_name, 'rb') as f:
    #    model3 = pickle.load(f)
    #print(model3.predict(scaler.transform(testData)))
    #print(model3.predict_proba(scaler.transform(testData)))
    # 評估模型3 Logistic Regression
    #print("Testing ...")
    # 計算訓練資料集的準確度
    # X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = logreg.score(test_X.values, test_y.values)
    print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))
    # print(logreg.predict(scaler.transform(testData)))
    # print(logreg.predict_proba(scaler.transform(testData)))
    # 儲存模型
    model_file_name = savePath+'NF_logisticregression.pickle'
    #return logreg
    with open(model_file_name, 'wb') as f:
        pickle.dump(logreg, f)
    acc.append(accuracy)
    y_pred = logreg.predict(X_train_final)
    mcc.append(matthews_corrcoef(Y_train, y_pred))
    fpr, tpr, thresholds = roc_curve(Y_train, logreg.predict_proba(X_train_final)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(Y_train, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}

def supportVectorMachine(df,savePath):  # Support Vector Machine
    df=dropNotInTarget(df)
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler

    model = SVC(kernel='linear', C=10, gamma='auto', cache_size=1000,probability=True)
    scaler = StandardScaler()

    # 編碼後的X與Y
    X_train = df.iloc[:, :5]
    Y_train = df.iloc[:, 5]
    X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    # Class count
    count_class_0, count_class_1 = Y_train.value_counts()
    X_train_final=X_train
    Y_train_final=Y_train
    # Divide by class
    # print("Data Rescaling ...")
    # X_train_class_0 = X_train[Y_train == 0]
    # X_train_class_1 = X_train[Y_train == 1]
    # X_train_class_0_under = X_train_class_0.sample(
    #     X_train_class_1.shape[0])  # 174
    # X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    # X_train_final = X_train_under
    # Y_train_final = Y_train[X_train_under.index]

    # 資料標準化
    X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
    test_X=pd.DataFrame(scaler.transform(test_X))
    #print('X_train_final.shape：{}'.format(X_train_final.shape))
    #print('Y_train_final.shape：{}'.format(Y_train_final.shape))

    # 訓練模型5 Support Vector Machine
    #print("Training ...")
    model.fit(X_train_final, Y_train_final)

    # 評估模型5 Support Vector Machine
    #print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = model.score(test_X, test_y)
    print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))
    # print(model.predict(scaler.transform(testData)))
    # print(model.predict_proba(scaler.transform(testData)))
    # 儲存模型
    model_file_name = savePath+'NF_supportVectorMachine.pickle'
    #return model
    with open(model_file_name, 'wb') as f:
        pickle.dump(model, f)
    acc.append(accuracy)
    y_pred = model.predict(X_train_final)
    mcc.append(matthews_corrcoef(Y_train_final, y_pred))
    fpr, tpr, thresholds = roc_curve(Y_train_final, model.predict_proba(X_train_final)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(Y_train_final, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}
def neuralNetwork(df,savePath):
    df=dropNotInTarget(df)
    
    import numpy as np
    dataset = df.values
    np.random.shuffle(dataset)
    dataset = pd.DataFrame(dataset)
    X = dataset.iloc[:, :5]
    y = dataset.iloc[:, 5]
    # 定義模型
    from keras.models import Sequential
    from keras.layers import Dense, Activation
    from keras.layers import Dropout
    from sklearn.preprocessing import StandardScaler

    X_train=X
    y_train=y
    # X_train_class_0 = X[y == 0]
    # X_train_class_1 = X[y == 1]
    # X_train_class_0_under = X_train_class_0.sample(X_train_class_1.shape[0])
    # X_train_under = pd.concat([X_train_class_0_under, X_train_class_1], axis=0)
    # X_train = X_train_under
    # y_train = y[X_train_under.index]
    # X_train_mean = X_train.mean(axis=0)
    # X_train_std = X_train.std(axis=0)
    # print(X_train_mean)
    # print(X_train_std)

    #正規化
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype("float32")
    y_train = y_train.astype("float32")

    # 定義模型
    model = Sequential()
    model.add(Dense(28, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dropout(0.75))
    model.add(Dense(1,  activation='sigmoid'))

    # 顯示模型摘要資訊
    # print('模型摘要資訊：')
    # model.summary()


    # 編譯模型
    model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])

    # 訓練模型
    # print("Training ...")
    # X_train：訓練資料的特徵資料
    # Y_train：訓練資料的輸出欄位
    # validation_split：分割出驗證資料集的比例
    # epochs：訓練週期
    # batch_size：批次大小
    # verbose：訓練過程中訊息顯示的詳細程度
    model.fit(X_train, y_train, epochs=300,validation_split=0.1)

    # print("Testing ...")

    # 計算訓練資料集的準確度
    accuracy = model.evaluate(X_train, y_train)
    # print(accuracy)
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]

    X = pd.DataFrame(scaler.fit_transform(X))
    accuracy = model.evaluate(X, Y)
    # print(accuracy)
    
    # print("Saving Model: ...")
    model_file_name = 'NF_neuralNetwork.pickle'
    model.save(savePath+'NF_neuralNetwork.h5')

    acc.append(accuracy[1])
    y_pred = model.predict(X)
    y_pred = (y_pred > 0.5)
    mcc.append(matthews_corrcoef(Y, y_pred))
    fpr, tpr, thresholds = roc_curve(Y, model.predict(X))
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(Y, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}

if __name__==("__main__"):
    df=pd.read_csv('trainingData/NFdata1415.csv')
    # decisionTree(df,'')
    print(randomForest(df,''))
    # logisticregression(df,'')
    # supportVectorMachine(df,'')
    # neuralNetwork(df,'')
    # df=dropNotInTarget(df,True)
    # from sklearn.preprocessing import StandardScaler
    # scaler = StandardScaler()
    # df = pd.DataFrame(scaler.fit_transform(df))
    # from tensorflow.keras.models import load_model
    
    # model4 = load_model('NF_neuralNetwork.h5')
    
    # pred4 = model4.predict(np.array(scaler.transform(
    #     testData
    # )
    #     ))
    
    # print(pred4)
    # pred4 = pred4[0][0]