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
from sklearn.model_selection import RepeatedStratifiedKFold
#效能相關

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
def LR(df,savePath,split=80,fold=1):  # Logistic Regression
    # 資料處理3 Logistic Regression
    acc = []
    mcc = []
    auroc = []
    sen = []
    spe = []
    df=dropNotInTarget(df)
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    
    
    RSKF = RepeatedStratifiedKFold(n_splits=fold, n_repeats=10, random_state=87)
    X = df.iloc[:, :15]
    Y = df.iloc[:, 15]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]

            logreg = LogisticRegression()
            scaler = StandardScaler()

            
            count_class_0, count_class_1 = Y_train.value_counts()
            #填補遺漏值
            imp = SimpleImputer(missing_values=np.nan, strategy='mean')
            imp.fit(X_train)
            X_train = imp.transform(X_train)
            imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
            imp2.fit(test_X)
            test_X = imp2.transform(test_X)
        
            X_train_final = pd.DataFrame(scaler.fit_transform(X_train))
            test_X=pd.DataFrame(scaler.transform(test_X))
        
            logreg.fit(X_train_final.values, Y_train.values)

            
        
            accuracy = logreg.score(test_X.values, test_y.values)
            # print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))
        
            
            #return logreg
            if(accuracy>acc_max):
                best_model=logreg
                acc_max=accuracy
            acc.append(accuracy)
            y_pred = logreg.predict(X_train_final)
            mcc.append(matthews_corrcoef(Y_train, y_pred))
            fpr, tpr, thresholds = roc_curve(Y_train, logreg.predict_proba(X_train_final)[:,1])
            auroc.append(auc(fpr, tpr))
            C_matrix = confusion_matrix(Y_train, y_pred)
            sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
            spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
            #print(acc,mcc,auroc,sen,spe)
    else:
       

        logreg = LogisticRegression()
        scaler = StandardScaler()

        #填補遺漏值
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
        imp2.fit(test_X)
        test_X = imp2.transform(test_X)
        count_class_0, count_class_1 = Y_train.value_counts()

    
        X_train_final = pd.DataFrame(scaler.fit_transform(X_train))
        test_X=pd.DataFrame(scaler.transform(test_X))
    
        logreg.fit(X_train_final.values, Y_train.values)

        
    
        accuracy = logreg.score(test_X.values, test_y.values)
        # print("Logistic Regression 訓練資料集的準確度 = {:.4f}".format(accuracy))
    
        
        #return logreg
        if(accuracy>acc_max):
            best_model=logreg
            acc_max=accuracy
        acc.append(accuracy)
        y_pred = logreg.predict(X_train_final)
        mcc.append(matthews_corrcoef(Y_train, y_pred))
        fpr, tpr, thresholds = roc_curve(Y_train, logreg.predict_proba(X_train_final)[:,1])
        auroc.append(auc(fpr, tpr))
        C_matrix = confusion_matrix(Y_train, y_pred)
        sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
        spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    model_file_name = savePath+'sepsis_logisticregression.pickle'
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}

     
def RF(df,savePath,split=80,fold=1):  # Random forest
    # 資料處理2 Random forest
    acc = []
    mcc = []
    auroc = []
    sen = []
    spe = []
    df=dropNotInTarget(df)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    rf = RandomForestClassifier(
        n_estimators=100, max_depth=7, criterion='entropy', max_features='sqrt')
    scaler = StandardScaler()
    
    # 編碼後的X與Y
    RSKF = RepeatedStratifiedKFold(n_splits=fold, n_repeats=10, random_state=87)
    X = df.iloc[:, :15]
    Y = df.iloc[:, 15]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    # X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]
        # Class count
            #填補遺漏值
            imp = SimpleImputer(missing_values=np.nan, strategy='mean')
            imp.fit(X_train)
            X_train = imp.transform(X_train)
            imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
            imp2.fit(test_X)
            test_X = imp2.transform(test_X)
            count_class_0, count_class_1 = Y_train.value_counts()
            X_train_final=X_train
            Y_train_final=Y_train
        
            X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
            test_X = pd.DataFrame(scaler.fit_transform(test_X))
        
            rf.fit(X_train_final, Y_train_final)

        
            accuracy = rf.score(test_X, test_y)
            # print("Random forest 訓練資料集的準確度 = {:.4f}".format(accuracy))
            if(accuracy>acc_max):
                best_model=rf
                acc_max=accuracy
            acc.append(accuracy)
            y_pred = rf.predict(X_train_final)
            mcc.append(matthews_corrcoef(Y_train_final, y_pred))
            fpr, tpr, thresholds = roc_curve(Y_train_final, rf.predict_proba(X_train_final)[:,1])
            auroc.append(auc(fpr, tpr))
            C_matrix = confusion_matrix(Y_train_final, y_pred)
            sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
            spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    else:
        #填補遺漏值
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
        imp2.fit(test_X)
        test_X = imp2.transform(test_X)
        count_class_0, count_class_1 = Y_train.value_counts()
        X_train_final=X_train
        Y_train_final=Y_train
    
        X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
        test_X = pd.DataFrame(scaler.fit_transform(test_X))
    
        rf.fit(X_train_final, Y_train_final)

    
        accuracy = rf.score(test_X, test_y)
        # print("Random forest 訓練資料集的準確度 = {:.4f}".format(accuracy))
        if(accuracy>acc_max):
            best_model=rf
            acc_max=accuracy
    
        
        acc.append(accuracy)
        y_pred = rf.predict(X_train_final)
        mcc.append(matthews_corrcoef(Y_train_final, y_pred))
        fpr, tpr, thresholds = roc_curve(Y_train_final, rf.predict_proba(X_train_final)[:,1])
        auroc.append(auc(fpr, tpr))
        C_matrix = confusion_matrix(Y_train_final, y_pred)
        sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
        spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    model_file_name = savePath+'sepsis_randomForest.pickle'
    #return rf
    #imf=rf.feature_importances_
    # print(imf)
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}

def SVM(df,savePath,split=80,fold=1):  # Support Vector Machine
    df=dropNotInTarget(df)
    acc = []
    mcc = []
    auroc = []
    sen = []
    spe = []
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler

    model = SVC(kernel='linear', C=10, gamma='auto', cache_size=1000,probability=True)
    scaler = StandardScaler()

    # 編碼後的X與Y
    RSKF = RepeatedStratifiedKFold(n_splits=fold, n_repeats=10, random_state=87)
    X = df.iloc[:, :15]
    Y = df.iloc[:, 15]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    # X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]  
            count_class_0, count_class_1 = Y_train.value_counts()
            
            
             #填補遺漏值
            imp = SimpleImputer(missing_values=np.nan, strategy='mean')
            imp.fit(X_train)
            X_train = imp.transform(X_train)
            imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
            imp2.fit(test_X)
            test_X = imp2.transform(test_X)
            X_train_final=X_train
            Y_train_final=Y_train
        
            X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
            test_X=pd.DataFrame(scaler.transform(test_X))
            model.fit(X_train_final, Y_train_final)

            X_train = pd.DataFrame(scaler.fit_transform(X_train))
            accuracy = model.score(test_X, test_y)
            # print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))
        
            
            if(accuracy>acc_max):
                best_model=model
                acc_max=accuracy
            acc.append(accuracy)
            y_pred = model.predict(X_train_final)
            mcc.append(matthews_corrcoef(Y_train_final, y_pred))
            fpr, tpr, thresholds = roc_curve(Y_train_final, model.predict_proba(X_train_final)[:,1])
            auroc.append(auc(fpr, tpr))
            C_matrix = confusion_matrix(Y_train_final, y_pred)
            sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
            spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    else:
        count_class_0, count_class_1 = Y_train.value_counts()
        
        #填補遺漏值
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        imp.fit(X_train)
        X_train = imp.transform(X_train)
        imp2=SimpleImputer(missing_values=np.nan, strategy='mean')
        imp2.fit(test_X)
        test_X = imp2.transform(test_X)
        
        X_train_final=X_train
        Y_train_final=Y_train
    
        X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
        test_X=pd.DataFrame(scaler.transform(test_X))
        model.fit(X_train_final, Y_train_final)

        X_train = pd.DataFrame(scaler.fit_transform(X_train))
        accuracy = model.score(test_X, test_y)
        # print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))
    
        
        #return model
        if(accuracy>acc_max):
            best_model=model
            acc_max=accuracy
        acc.append(accuracy)
        y_pred = model.predict(X_train_final)
        mcc.append(matthews_corrcoef(Y_train_final, y_pred))
        fpr, tpr, thresholds = roc_curve(Y_train_final, model.predict_proba(X_train_final)[:,1])
        auroc.append(auc(fpr, tpr))
        C_matrix = confusion_matrix(Y_train_final, y_pred)
        sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
        spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    #print(acc,mcc,auroc,sen,spe)
    model_file_name = savePath+'sepsis_supportVectorMachine.pickle'
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}
def testPredict():
    #load data from csv
    df=pd.read_csv('trainingData/15TB.csv',encoding='big5')#,encoding='utf-8-sig')
    df.drop(columns='ID',inplace=True)
    # print(df)
    df=getItemInOrder(df)
    #load model
    model_file_name = 'sepsis_supportVectorMachine.pickle'
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
    df=pd.read_csv('trainingData/Sepsis_15TB.csv',encoding='utf-8-sig')
    # df.drop('ID',axis=1,inplace=True)
    # print(pd.DataFrame(df).values)
    lr=LR(df,'',80,5)
    rf=RF(df,'',80,5)
    svm=SVM(df,'',80,5)
    print(lr)
    print(rf)
    print(svm)
    testPredict()