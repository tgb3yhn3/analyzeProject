import pandas as pd
from scipy import stats
import math as Math
def p_value(df=pd.read_csv("trainingData/NFdata1415.csv",encoding="utf-8-sig"),target=['sea','wbc','crp','seg','band'],type="nf"):
    column_headers = list(df.columns)
    rtn=[]
    for i in range(len(column_headers)):
        #print(column_headers[i])
        
        if(column_headers[i] in target or type=='sepsis'):
            if(type=='sepsis'):
                crosstab = pd.crosstab(df[column_headers[i]],df["sofa_sepsis"])
            else:
                crosstab = pd.crosstab(df[column_headers[i]],df["nf"])
            
            #print(crosstab)
            crosstab, p_value, degFreedom, expected = stats.chi2_contingency(crosstab)
            #print("  ")
            #print("%s p-value = %.8f" %(column_headers[i],p_value))
            rtn.append([column_headers[i],p_value])
    return rtn
    #print("  ")
def meanStdCounter(df=pd.read_csv("trainingData/NFdata1415.csv",encoding="utf-8-sig"),target=['wbc','crp','seg','band']):
    column_headers = list(df.columns)
    rtn=[]
    for i in range(len(column_headers)):
        #print(column_headers[i])
        l=['wbc','crp','seg','band']
        if(column_headers[i] in target):
            rtn.append([column_headers[i],df[column_headers[i]].mean(),df[column_headers[i]].std()])
    return rtn

def pure_pvalue(df):
    column_headers = list(df.columns)
    
    if "sofa_sepsis" in column_headers:
        df_target = df["sofa_sepsis"]
    elif "nf" in column_headers:
        df_target = df["nf"]
    rtn=[]
    for i in range(len(column_headers)):
        crosstab = pd.crosstab(df[column_headers[i]],df_target)
        crosstab, p_value, degFreedom, expected = stats.chi2_contingency(crosstab)
        rtn.append("{:.2e}".format(p_value))
    return rtn
def pure_meanStd(df):
    column_headers = list(df.columns)
    rtn=[]
    for i in range(len(column_headers)):
        
        try:
            rtn.append([round(df[column_headers[i]].mean(),2),round(df[column_headers[i]].std(),2)])
        except:
            rtn.append([-1,-1])
    return rtn
def countGetDiease(df):
    column_headers = list(df.columns)
    if("nf" in column_headers):
        target = "nf"
    elif("sofa_sepsis" in column_headers):
        target = "sofa_sepsis"
    rtn=[]
    nonNFCount, c_counter = df[df[target]==0].shape
    nfCount, c_counter = df[df[target]==1].shape
    column_headers = list(df.columns)
    for i in range(len(column_headers)):
        df2 = df[df[column_headers[i]]==1]
        nfCount2, c_counter = df2[df2[target]==1].shape
        nonNFCount2, c_counter = df2[df2[target]==0].shape
        nfPercent2=nfCount2*100/nfCount
        nonNFPercent2=nonNFCount2*100/nonNFCount
        rtn.append([nfCount2,round(nfPercent2,2),nonNFCount2,round(nonNFPercent2,2)])
        # print("NF/nonNF %s positive count(percent) = %d (%.1f%%) / %d (%.1f%%)" %(column_headers[i],nfCount2,nfPercent2,nonNFCount2,nonNFPercent2))
    return rtn
def countGetDiseaseValueType(df)->list:
    column_headers = list(df.columns)
    if("nf" in column_headers):
        target = "nf"
    elif("sofa_sepsis" in column_headers):
        target = "sofa_sepsis"
    mask = df[target]==1      #記錄NF的資料
    dfA = df[mask]				#指定訓練資料
    dfB = df[~mask]

    column_headers = list(df.columns)
    rtn=[]
    for i in range(len(column_headers)):
    #Perform two-sided Mann-Whitney U test (Two columns do not have equal medians).
        uStatistic, p_value = stats.mannwhitneyu(x=dfA[column_headers[i]], y=dfB[column_headers[i]], alternative="two-sided")
        rtn.append("{:.2e}".format(p_value))
    return rtn
def findIsValueType(row):
    #if only have 1 and 0
    for i in row:
        if(i!=0 and i!=1):
            return True
    return False
if(__name__=="__main__"):
    df=pd.read_csv('危險因子分析/NFdata1415.csv',encoding='utf-8-sig')
    countGetDiease(df)
    # print(pure_pvalue(df))
    # print(meanStdCounter(df))