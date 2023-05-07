import pandas as pd
import pickle
import tools.modelTrainingNF as NF 
import tools.modelTrainingSepsis as Sepsis
# 讀取資料集
def training(df,filename="",savePath="static/model/",modelType="NF"):
    #if(df):
     #   df = pd.read_csv(filename)
    #print(df)
    # 顯示資料集的描述資料
    print('資料集的描述：')
    print(df.describe())

    # 顯示沒有資料的筆數
    print('沒有資料的筆數：')
    print(df.isnull().sum())
    rtn={}
    try:
        if(modelType=="NF"):
            rtn= {"dt":NF.decisionTree(df,savePath),
            "rf":NF.randomForest(df,savePath),
            "lr":NF.logisticregression(df,savePath),
            "svm":NF.supportVectorMachine(df,savePath),
            "nl":NF.neuralNetwork(df,savePath)}
        #return model
        elif (modelType=="Sepsis"):
            rtn= {"lr":Sepsis.LR(df,savePath),
            "rf":Sepsis.RF(df,savePath),
            "svm":Sepsis.SVM(df,savePath)}
    except Exception as e:
        print(e.with_traceback())
        return None
    return rtn



if __name__=="__main__":
    df = pd.read_csv("trainingData/NFdata1415.csv",encoding="utf-8-sig")
    training(df,modelType="NF")
    df = pd.read_csv("trainingData/15TB2.csv",encoding="utf-8-sig")
    training(df,modelType="Sepsis")
# decisionTree()
# randomForest()
# logisticregression()
# supportVectorMachine()
