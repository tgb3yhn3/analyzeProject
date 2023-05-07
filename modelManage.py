import datetime
import json
import shutil
from flask import Flask, Response, redirect, render_template, request, url_for,Blueprint
import os
import sqlite3
import tools2.modelTraining as modelTraining
import pandas as pd
dbfile = "modelDB.db"


modelManger=Blueprint('modelManger',__name__,template_folder='templates',static_folder='static')


#query data from database
def getData(strSQL):
    conn = sqlite3.connect(dbfile)
    #print(strSQL)
    rows = conn.execute(strSQL)
    #print(rows.arraysize)
    return rows

#save model to database
def saveModel(startDate,endDate,fileName,modelType):
    conn= sqlite3.connect(dbfile)
    cursor = conn.cursor()
    nowTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #file=convertToBinaryData(file)
    #insert data into table startDate,endDate,modelVersion,datasetName,model
    cursor.execute("INSERT INTO model (startDate,endDate,updateDate,datasetName,type) VALUES (?,?,?,?,?)",(startDate,endDate,nowTime,fileName,modelType))
    #check if insert success
    if cursor.rowcount < 1:
        return False
    else:
        conn.commit()

    return True

#check if modelVersion is in use
def checkIsuse(modelVersion,modelType):
    conn= sqlite3.connect(dbfile)
    cursor = conn.cursor()
    if modelType=="NF":
        cursor.execute("SELECT modelVersionNF FROM nowUseModel order by id desc limit 1")
    elif modelType=="Sepsis":
        cursor.execute("SELECT modelVersionSepsis FROM nowUseModel order by id desc limit 1")
    if cursor.fetchone()==None:
        return False
    #if modelVersion is in use
    if cursor.fetchone()==modelVersion:
        return True
    else:
        return False
    
def getNowUseModel():
    conn= sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nowUseModel order by id desc limit 1")
    return cursor.fetchone()
def parse_json(data):
    print(data)
    if data:
        return json.loads(data)
    else:
        return None
#query model by modelVersion or datasetName
@modelManger.route('/model',methods=['GET'])
def queryModel():
    #get queryString
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    modelVersion = request.args.get('modelVersion')
    modelType= request.args.get('type')
    
    queryString="select * from model M left join modelEfficacy ME on M.modelVersion=ME.modelVersion where 1=1 "
    if startDate:
        queryString+=" and startDate=\""+startDate+"\""
    if endDate:
        queryString+=" and endDate=\""+endDate+"\""
    if modelVersion:
        queryString+=" and modelVersion="+modelVersion
    if modelType:
        queryString+=" and type=\""+modelType+"\""
    queryString+=" order by modelVersion desc"
    print(queryString)
        
    #get data from database
    data=getData(queryString).fetchall()
    #check if data not found
    # if   len(data)< 1:
    #     return "data not found"
    # else:
    json_list=[]
    for i in data:
        if(i[7]!=None):
            json_list.append(json.loads(i[7]))
        else:
            json_list.append(None)
    return render_template("model.html",models=data,nowUse=getNowUseModel(),modelEfficacy=json_list)

#upload model
@modelManger.route('/model',methods=['POST'])
def uploadModel():
    #upload file
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    file = request.files['file']
    modelType= request.form['type']
    #getfilename from form
    fileName = file.filename
    #read file use panda
    df = pd.read_csv(file,encoding='utf-8-sig')
    #get max modelVersion
    data=getData("select seq from sqlite_sequence where name=\"model\" ")
    #if nodata set modelVersion=1
    modelVersion=data.fetchone()[0]
    if modelVersion==None:
        modelVersion="1"
    else:
        modelVersion=str(int(modelVersion)+1)
    try:
        model=modelTraining.training(df,filename="",savePath="modelData/"+modelVersion+"_",modelType=modelType)
    except:
        return "400 training error your modelType:"+modelType +" your upload file:"+fileName
    if model!=None and saveModel(startDate,endDate,fileName,modelType):
        # turn dict to json
        model=json.dumps(model)
        #get last modelVersion
        data=getData("select seq from sqlite_sequence where name=\"model\" ")
        modelVersion=data.fetchone()[0]
        #save json to db
        conn= sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO modelEfficacy (modelVersion,jsonData) VALUES (?,?)",(modelVersion,model))
        conn.commit()

    


        return redirect(url_for('modelManger.queryModel'))
    else:
        return "fail" 

#delete model by modelVersion
@modelManger.route('/model',methods=['DELETE'])
def deleteModel():
    #get modelVersion
    modelVersion = request.form['modelVersion']
    modelType= request.form['type']
    #delete modelVersion
    if checkIsuse(modelVersion,modelType):
        return "400 model is in use"
    conn= sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM model WHERE modelVersion="+modelVersion+" and type=\""+modelType+"\"" )
    #check if delete success
    if  cursor.rowcount < 1:
        return "400 delete fail"
    else:
        conn.commit()
    #delete modelFile
    if(modelType=="NF"):
        os.remove("modelData/"+modelVersion+"_NF_decisionTree.pickle")
        os.remove("modelData/"+modelVersion+"_NF_randomForest.pickle")
        os.remove("modelData/"+modelVersion+"_NF_logisticregression.pickle")
        os.remove("modelData/"+modelVersion+"_NF_supportVectorMachine.pickle")
    elif(modelType=="Sepsis"):
        os.remove("modelData/"+modelVersion+"_Sepsis_randomForest.pickle")
        os.remove("modelData/"+modelVersion+"_Sepsis_logisticregression.pickle")
        os.remove("modelData/"+modelVersion+"_Sepsis_supportVectorMachine.pickle")
    return "200 success"

#replace current model file at static/model from modelData folder
@modelManger.route('/model/select',methods=['POST'])
def replaceModel():
    modelVersion=request.form['modelVersion']
    modelType=request.form['type']
    modellist_NF=[
        'NF_decisionTree.pickle',
        'NF_randomForest.pickle',
        'NF_logisticRegression.pickle',
        'NF_supportVectorMachine.pickle',
        'NF_neuralNetWork.h5'
    ]
    modellist_Sepsis=[
        'sepsis_randomForest.pickle',
        'sepsis_logisticRegression.pickle',
        'sepsis_supportVectorMachine.pickle'
    ]
    if modelType=="NF":
        modellist=modellist_NF
    else:
        modellist=modellist_Sepsis
    #get model file from modelData folder
    for model in modellist:
        modellist[modellist.index(model)]=model.format(modelVersion)
    #check if model file exist
    for model in modellist:
        if not os.path.exists('modelData/'+str(modelVersion)+"_"+model):
            writeLog('model file not exist ' +str(modelVersion)+"_"+model)
            print('model file not exist ' +str(modelVersion)+"_"+model)
            return Response(status="400")

    #copy model file at static/model
    for model in modellist:
        shutil.copyfile('modelData/'+str(modelVersion)+"_"+model,'static/model/'+model)
        

       
    #update modelVersion to DB
    if not updateVersion(modelVersion,modelType):
        return "400"
    return "200"


        

#do predict with modelVersion
@modelManger.route('/predict/NF/<modelVersion>',methods=['GET'])
def predict(modelVersion):
    #TODO
    #get data from database
    data=getData("select * from model where modelVersion="+modelVersion)
    #get modelFile
    if data.rowcount < 1:
        return "fail"
    else:
        modelFile=data[0][4]
        #do predict
    

    return "success"

#writelog to log file
def writeLog(log):
    #write log to log file file name is now time
    nowTime = datetime.datetime.now().strftime("%Y%m%d")
    with open('log/log'+nowTime, 'a') as file:
        file.write(log)
#update model Version to DB  (modelVersion,updateDate)
def updateVersion(modelVersion,modelType="NF"):
    conn= sqlite3.connect(dbfile)
    cursor = conn.cursor()
    #get NF modelVersion
    if modelType=="NF":
        #the sepsis didn't need to update
        cursor.execute("select modelVersionSepsis from nowUseModel order by id desc limit 1")
        modelVersionSepsis=cursor.fetchone()
        if modelVersionSepsis==None:
            modelVersionSepsis=[""]
        cursor.execute("insert into nowUseModel (modelVersionNF,modelVersionSepsis,updateDate) values (?,?,?)",(modelVersion,modelVersionSepsis[0],datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    else:
        #the NF didn't need to update
        cursor.execute("select modelVersionNF from nowUseModel order by id desc limit 1")
        modelVersionNF=cursor.fetchone()
        if modelVersionNF==None:
            modelVersionNF=[""]
        cursor.execute("insert into nowUseModel (modelVersionNF,modelVersionSepsis,updateDate) values (?,?,?)",(modelVersionNF[0],modelVersion,datetime.datetime.now().strftime("%Y%m%d%H%M%S")))    
    #check if insert success
    conn.commit()
    return True

     



if __name__ == '__main__':

    
    app.run(debug=True)


