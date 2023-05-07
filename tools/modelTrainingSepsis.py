# RF
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np


import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, confusion_matrix, matthews_corrcoef, roc_curve
#效能相關
acc = []
mcc = []
auroc = []
sen = []
spe = []

def LR(df,savePath):
    alldata = df.values
    #np.random.shuffle(alldata)
    alldata = pd.DataFrame(alldata, columns=df.columns)
    X = alldata.iloc[:,:15]
    y = alldata.iloc[:,15]
    logreg = LogisticRegression(C= 1, penalty= 'l2')

    X_train, X_test = X.iloc[::2], X.iloc[1::2]
    y_train, y_test = y.iloc[::2], y.iloc[1::2]

    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    X_test = imp.transform(X_test)

    #正規化
    X_train_mean = X_train.mean(axis=0)
    X_train_std = X_train.std(axis=0)
    #print(X_train_mean)
    #print(X_train_std)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype('float64')
    X_test = pd.DataFrame(scaler.transform(X_test)).astype('float64')
    y_train=y_train.astype('int')
    y_test=y_test.astype('int')
    # 訓練模型3 Logistic Regression
    print("Training ...")
    logreg.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = logreg.score(X_test, y_test)
    print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'sepsis_logisticregression.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(logreg, f)
    acc.append(accuracy)
    y_pred = logreg.predict(X_test)
    mcc.append(matthews_corrcoef(y_test, y_pred))
    fpr, tpr, thresholds = roc_curve(y_test, logreg.decision_function(X_test))
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(y_test, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe) 
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}
     
def RF(df,savePath):
    from sklearn.ensemble import RandomForestClassifier

    rf = RandomForestClassifier(criterion= 'entropy', max_depth= 10, max_features= 'sqrt', n_estimators= 100)

    alldata = df.values
    #np.random.shuffle(alldata)
    alldata = pd.DataFrame(alldata, columns=df.columns[0:297])
    X = alldata.iloc[:,:15]
    y = alldata.iloc[:,15]

    X_train, X_test = X.iloc[::2], X.iloc[1::2]
    y_train, y_test = y.iloc[::2], y.iloc[1::2]


    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    X_test = imp.transform(X_test)

    #正規化
    X_train_mean = X_train.mean(axis=0)
    X_train_std = X_train.std(axis=0)
    #print(X_train_mean)
    #print(X_train_std)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype('float64')
    X_test = pd.DataFrame(scaler.transform(X_test)).astype('float64')
    y_train=y_train.astype('float64')
    y_test=y_test.astype('float64')

    # 訓練模型3 Logistic Regression
    print("Training ...")
    rf.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = rf.score(X_test, y_test)
    print("Random Forest 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'sepsis_randomForest.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(rf, f)
    acc.append(rf.score(X_test, y_test))
    y_pred = rf.predict(X_test)
    mcc.append(matthews_corrcoef(y_test, y_pred))
    fpr, tpr, thresholds = roc_curve(y_test, rf.predict_proba(X_test)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(y_test, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}
def SVM(df,savePath):
    from sklearn.pipeline import Pipeline
    from sklearn.svm import SVC

    svm = SVC(C= 10, gamma= 0.01, kernel= 'sigmoid',probability=True, max_iter = -1)
    alldata = df.values
    #np.random.shuffle(alldata)
    alldata = pd.DataFrame(alldata, columns=df.columns[0:297])
    X = alldata.iloc[:,:15]
    y = alldata.iloc[:,15]
    X_train, X_test = X.iloc[::2], X.iloc[1::3]
    y_train, y_test = y.iloc[::2], y.iloc[1::3]

    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    X_test = imp.transform(X_test)

    #正規化
    X_train_mean = X_train.mean(axis=0)
    X_train_std = X_train.std(axis=0)
    #print(X_train_mean)
    #print(X_train_std)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype('float64')
    X_test = pd.DataFrame(scaler.transform(X_test)).astype('float64')
    y_train=y_train.astype('float64')
    y_test=y_test.astype('float64')


    # 訓練模型3 Logistic Regression
    print("Training ...")
    svm.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = svm.score(X_test, y_test)
    print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))

    # 儲存模型
    model_file_name = savePath+'sepsis_supportVectorMachine.pickle'
    with open(model_file_name, 'wb') as f:
        pickle.dump(svm, f)
    acc.append(svm.score(X_test, y_test))
    y_pred = svm.predict(X_test)
    mcc.append(matthews_corrcoef(y_test, y_pred))
    fpr, tpr, thresholds = roc_curve(y_test, svm.predict_proba(X_test)[:,1])
    auroc.append(auc(fpr, tpr))
    C_matrix = confusion_matrix(y_test, y_pred)
    sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
    spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':acc[-1],'mcc':mcc[-1],'auroc':auroc[-1],'sen':sen[-1],'spe':spe[-1]}
if __name__=='__main__':
    df=pd.read_csv('sepsis.csv',encoding='utf-8-sig')
    df.drop('ID',axis=1,inplace=True)
    lr=LR(df,'')
    rf=RF(df,'')
    svm=SVM(df,'')
    print(lr,rf,svm)