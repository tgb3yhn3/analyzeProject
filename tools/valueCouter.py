import pandas as pd
from scipy import stats
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
if(__name__=="__main__"):
    df=pd.read_csv('危險因子分析/NFdata1415.csv',encoding='utf-8-sig')
    print(p_value(df))
    print(meanStdCounter(df))