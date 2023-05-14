# RF
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.model_selection import train_test_split

import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, confusion_matrix, matthews_corrcoef, roc_curve
#效能相關
acc = []
mcc = []
auroc = []
sen = []
spe = []
target=['gcs','meds_ams15b','meds_plt150b','sofa_res','sofa_ner','sofa_liver','sofa_coag','sofa_renal','bun','cre','plt','FIO2_percent','PF_ratio','fio2_per','fio2_cb','sofa_sepsis']
target2=['sea','wbc','crp','seg','band']
#get column which is in order of target  
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
        
def dropNotInTarget(df,isneu=True):
    return getItemInOrder(df)
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
def LR(df,savePath):
    
    df=dropNotInTarget(df)
    alldata = df.values
    #np.random.shuffle(alldata)
    alldata = pd.DataFrame(alldata)
    X = alldata.iloc[:,:15]
    # print(X)
    y = alldata.iloc[:,15]
    logreg = LogisticRegression(C= 1, penalty= 'l2')

    
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8,shuffle=True)
    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    X_test = imp.transform(X_test)
    X_train,X_test,y_train,y_test=train_test_split(X_train,y_train,train_size=0.8,shuffle=True)
    #正規化

    #print(X_train_mean)
    #print(X_train_std)
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype('float64')
    X_test = pd.DataFrame(scaler.transform(X_test)).astype('float64')
    # y_train=y_train.astype('int')
    # y_test=y_test.astype('int')
    # 訓練模型3 Logistic Regression
    # print("Training ...")
    logreg.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    # print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = logreg.score(X_test, y_test)
    print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))
    #print(logreg.feature_importances_)
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
    alldata = pd.DataFrame(alldata)
    X = alldata.iloc[:,:15]
    y = alldata.iloc[:,15]

    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8,shuffle=True)


    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    imp.fit(X_test)
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
    # print("Training ...")
    rf.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    # print("Testing ...")
    # 計算訓練資料集的準確度
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    accuracy = rf.score(X_test, y_test)
    print("Random Forest 訓練資料集的準確度 = {:.4f}".format(accuracy))
    # print(rf.feature_importances_)
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

    svm = SVC(C= 10, gamma='auto', kernel= 'linear',probability=True, max_iter = -1)
    alldata = df.values
    #np.random.shuffle(alldata)
    alldata = pd.DataFrame(alldata)
    X = alldata.iloc[:,:15]
    y = alldata.iloc[:,15]
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8,shuffle=True)

    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
    imp2.fit(X_test)
    X_test = imp2.transform(X_test)

    #正規化
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    X_test = pd.DataFrame(scaler.transform(X_test))


    # 訓練模型3 Logistic Regression
    # print("Training ...")
    svm.fit(X_train, y_train)

    # 評估模型3 Logistic Regression
    # print("Testing ...")
    # 計算訓練資料集的準確度
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
def testPredict():
    #load data from csv
    df=pd.read_csv('trainingData/15TB.csv',encoding='big5')#,encoding='utf-8-sig')
    df.drop(columns='ID',inplace=True)
    # print(df)
    df=getItemInOrder(df)
    #load model
    model_file_name = 'sepsis_randomForest.pickle'
    with open(model_file_name, 'rb') as f:
        rf = pickle.load(f)
    #predict
    df=dropNotInTarget(df)
    X=df.iloc[:,:15]
    y=df.iloc[:,15]
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8,shuffle=True)
    #填補遺漏值
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(X_train)
    X_train = imp.transform(X_train)
    imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
    imp2.fit(X_test)
    X_test = imp2.transform(X_test)
    #正規化
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train))
    X_test = pd.DataFrame(scaler.transform(X_test))
    #predict
    y_pred = rf.predict(X_test)
    # print(y_pred)
    # print(y_test)
    # print(y_pred==y_test)
    # print(y_pred==y_test)
    #count correct rate
    correct=0
    for i in range(len(y_pred)):
        if y_pred[i]==y_test.iloc[i]:
            correct+=1
    print("正確率：{:.2f}%".format(correct/len(y_pred)*100))
if __name__=='__main__':
    # df=pd.read_csv('trainingData/Sepsis_15TB.csv',encoding='utf-8-sig')
    # # df.drop('ID',axis=1,inplace=True)
    # print(pd.DataFrame(df).values)
    # lr=LR(df,'')
    # rf=RF(df,'')
    # svm=SVM(df,'')
    # print(lr,rf,svm)
    testPredict()