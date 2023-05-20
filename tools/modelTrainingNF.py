import numpy as np
import pandas as pd
import pickle
import math
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import Dropout
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import auc, confusion_matrix, matthews_corrcoef, roc_curve
from sklearn.model_selection import RepeatedStratifiedKFold
#效能相關

testData=[[
    1,12000,240,80,8
]]
target=['sea','wbc','crp','seg','band','nf']
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
def decisionTree(df,savePath,split=80,fold=1):  # Decision tree
    acc = []
    mcc = []
    auroc = []
    sen = []
    spe = []
    # 資料處理1 Decision tree
    df=dropNotInTarget(df)
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.preprocessing import StandardScaler
    
    clf = DecisionTreeClassifier(
        criterion='entropy', max_depth=5, min_samples_leaf=9,random_state=42)
    scaler = StandardScaler()

    # 編碼後的X與Y
    
    RSKF = RepeatedStratifiedKFold(n_splits=fold, n_repeats=10, random_state=87)
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]
            count_class_0, count_class_1 = Y_train.value_counts()
            X_train_final=X_train
            Y_train_final=Y_train
            
            X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
            test_X = pd.DataFrame(scaler.fit_transform(test_X))
        
            clf.fit(X_train_final, Y_train_final)

        
            accuracy = clf.score(test_X, test_y)
            # print("Decision tree 訓練資料集的準確度 = {:.4f}".format(accuracy))
        
            if(accuracy>acc_max):
                acc_max=accuracy
                best_model=clf
            acc.append(accuracy)
            y_pred = clf.predict(X_train_final)
            mcc.append(matthews_corrcoef(Y_train_final, y_pred))
            fpr, tpr, thresholds = roc_curve(Y_train_final, clf.predict_proba(X_train_final)[:,1])
            auroc.append(auc(fpr, tpr))
            C_matrix = confusion_matrix(Y_train_final, y_pred)
            sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
            spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
            # Class count
    else:
        count_class_0, count_class_1 = Y_train.value_counts()
        X_train_final=X_train
        Y_train_final=Y_train
      

        X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
        test_X = pd.DataFrame(scaler.fit_transform(test_X))
      
        clf.fit(X_train_final, Y_train_final)

        accuracy = clf.score(test_X, test_y)
       
        if(accuracy>acc_max):
            acc_max=accuracy
            best_model=clf
        acc.append(accuracy)
        y_pred = clf.predict(X_train_final)
        mcc.append(matthews_corrcoef(Y_train_final, y_pred))
        fpr, tpr, thresholds = roc_curve(Y_train_final, clf.predict_proba(X_train_final)[:,1])
        auroc.append(auc(fpr, tpr))
        C_matrix = confusion_matrix(Y_train_final, y_pred)
        sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
        spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
          
    model_file_name = savePath+'NF_decisionTree.pickle'
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
            pickle.dump(best_model, f)   
    #return 平均效能
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}
     
    
        
def randomForest(df,savePath,split=80,fold=1):  # Random forest
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
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    # X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]
        # Class count
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
    model_file_name = savePath+'NF_randomForest.pickle'
    #return rf
    #imf=rf.feature_importances_
    # print(imf)
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    #print(acc,mcc,auroc,sen,spe)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}



def logisticregression(df,savePath,split=80,fold=1):  # Logistic Regression
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
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]

            logreg = LogisticRegression()
            scaler = StandardScaler()

            
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
            #print(acc,mcc,auroc,sen,spe)
    else:
       

        logreg = LogisticRegression()
        scaler = StandardScaler()

        
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
    model_file_name = savePath+'NF_logisticregression.pickle'
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}

def supportVectorMachine(df,savePath,split=80,fold=1):  # Support Vector Machine
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
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]
    acc_max=0
    best_model=None
        
    X_train,test_X,Y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    # X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    if fold!=1:
        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,Y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]  
            count_class_0, count_class_1 = Y_train.value_counts()
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
        X_train_final=X_train
        Y_train_final=Y_train
    
        X_train_final = pd.DataFrame(scaler.fit_transform(X_train_final))
        test_X=pd.DataFrame(scaler.transform(test_X))
    
        model.fit(X_train_final, Y_train_final)

        X_train = pd.DataFrame(scaler.fit_transform(X_train))
        accuracy = model.score(test_X, test_y)
        print("Support Vector Machine 訓練資料集的準確度 = {:.4f}".format(accuracy))
    
        
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
    model_file_name = savePath+'NF_supportVectorMachine.pickle'
    print("best acc:",acc_max)
    with open(model_file_name, 'wb') as f:
        pickle.dump(best_model, f)
    return {'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}
def neuralNetwork(df,savePath,split=80,fold=1):
    acc = []
    mcc = []
    auroc = []
    sen = []
    spe = []
    df=dropNotInTarget(df)
    

    dataset = df.values
    np.random.shuffle(dataset)
    dataset = pd.DataFrame(dataset)
    RSKF = RepeatedStratifiedKFold(n_splits=fold, n_repeats=10, random_state=87)
    X = df.iloc[:, :5]
    Y = df.iloc[:, 5]
    acc_max=0
    best_model=None
        
    X_train,test_X,y_train,test_y=train_test_split(X,Y,train_size=split/100,shuffle=True)
    # X_train,test_X,Y_train,test_y=train_test_split(X_train,Y_train,train_size=0.8,shuffle=True)
    if fold!=1:
    # X = dataset.iloc[:, :5]
    # y = dataset.iloc[:, 5]
    # 定義模型
    

        for train_index, test_index in RSKF.split(X, Y):
            X_train,test_X,y_train,test_y=X.iloc[train_index],X.iloc[test_index],Y.iloc[train_index],Y.iloc[test_index]
            scaler = StandardScaler()
            X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype("float32")
            test_X=pd.DataFrame(scaler.transform(test_X)).astype("float32")
            y_train = y_train.astype("float32")

            
            model = Sequential()
            model.add(Dense(28, input_dim=X_train.shape[1], activation='relu'))
            model.add(Dropout(0.75))
            model.add(Dense(1,  activation='sigmoid'))
            model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])

            
            model.fit(X_train, y_train, epochs=100,validation_split=0.1,verbose=0)

        
            # accuracy = model.evaluate(X_train, y_train)
            # print(accuracy)

            accuracy = model.evaluate(test_X, test_y,verbose=0)
            # print(accuracy[1])
            
            # print("Saving Model: ...")
            if(accuracy[1]>acc_max):
                acc_max=accuracy[1]
                best_model=model

            acc.append(accuracy[1])
            y_pred = model.predict(X_train)
            y_pred = (y_pred > 0.5)
            mcc.append(matthews_corrcoef(y_train, y_pred))
            fpr, tpr, thresholds = roc_curve(y_train, model.predict(X_train))
            auroc.append(auc(fpr, tpr))
            C_matrix = confusion_matrix(y_train, y_pred)
            sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
            spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))
    else:
        scaler = StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train)).astype("float32")
        y_train = y_train.astype("float32")
        test_X=pd.DataFrame(scaler.transform(test_X)).astype("float32")

        
        model = Sequential()
        model.add(Dense(28, input_dim=X_train.shape[1], activation='relu'))
        model.add(Dropout(0.75))
        model.add(Dense(1,  activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])

        
        model.fit(X_train, y_train, epochs=100,validation_split=0.1,verbose=0)

    
        accuracy = model.evaluate(X_train, y_train,verbose=0)
        # print(accuracy)
# accuracy = model.evaluate(X_train, y_train)
            # print(accuracy)
      
        accuracy = model.evaluate(test_X, test_y,verbose=0)
        # print(accuracy)
        
        # print("Saving Model: ...")
        if(accuracy[1]>acc_max):
            acc_max=accuracy[1]
            best_model=model
        acc.append(accuracy[1])
        y_pred = model.predict(X_train)
        y_pred = (y_pred > 0.5)
        mcc.append(matthews_corrcoef(y_train, y_pred))
        fpr, tpr, thresholds = roc_curve(y_train, model.predict(X_train))
        auroc.append(auc(fpr, tpr))
        C_matrix = confusion_matrix(y_train, y_pred)
        sen.append(C_matrix[1,1]/(C_matrix[1,1]+C_matrix[1,0]))
        spe.append(C_matrix[0,0]/(C_matrix[0,0]+C_matrix[0,1]))      
    #print(acc,mcc,auroc,sen,spe)
    print("best acc",acc_max)
    model_file_name = 'NF_neuralNetwork.pickle'
    best_model.save(savePath+'NF_neuralNetwork.h5')
    return{'acc':np.mean(acc),'mcc':np.mean(mcc),'auroc':np.mean(auroc),'sen':np.mean(sen),'spe':np.mean(spe)}

if __name__==("__main__"):
    df=pd.read_csv('trainingData/NFdata1415.csv')
    # print(decisionTree(df,'',80,1))
    # print(randomForest(df,'',80,5))
    # print(logisticregression(df,'',80,10))
    # print(supportVectorMachine(df,'',80,1))
    print(neuralNetwork(df,'',80,1))    
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