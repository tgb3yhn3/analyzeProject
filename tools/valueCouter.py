import pandas as pd
from scipy import stats
def p_value(df=pd.read_csv("trainingData/NFdata1415.csv",encoding="utf-8-sig")):
    column_headers = list(df.columns)
    rtn=[]
    for i in range(len(column_headers)):
        #print(column_headers[i])
        l=['wbc','crp','seg','band']
        if(column_headers[i] in l):
            crosstab = pd.crosstab(df[column_headers[i]],df["nf"])
            #print(crosstab)
            crosstab, p_value, degFreedom, expected = stats.chi2_contingency(crosstab)
            #print("  ")
            #print("%s p-value = %.8f" %(column_headers[i],p_value))
            rtn.append([column_headers[i],p_value])
    return rtn
    #print("  ")
if(__name__=="__main__"):
    df=pd.read_csv('trainingData/NFdata1415.csv',encoding='utf-8-sig')
    print(p_value(df))