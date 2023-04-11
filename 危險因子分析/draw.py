import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
def drawImg(df_ori):

    
    column_headers = list(df_ori.columns)
    max_values=[]
    name_list=['wbc','wbc','seg','seg','band','band']
    
    fig = plt.figure(figsize=(16, 9))
    
    ax = fig.subplots(1, 6)
    # mgr = plt.get_current_fig_manager()

    # 切換至全螢幕模式
    # mgr.full_screen_toggle()        
    for index,i in enumerate(name_list):
        # column_headers=df[i]
        df=df_ori[df_ori['nf']==index%2]
        
        sns.boxplot(x='nf', y=i, data=df,ax=ax[index])
        #ax[index].tick_params(axis='x', labelleft=False, labelright=True)
        q1, q2, q3 = df[i].quantile(q=[0.25, 0.5, 0.75])
        max_val=df[i].max()
        # 繪製平均值、中位數和四分位數
        ax[index].axhline(df[i].mean(), color='r', linestyle='--', label='mean')
        ax[index].axhline(q1, color='g', linestyle='--', label='q1')
        ax[index].axhline(q2, color='b', linestyle='--', label='q2')
        ax[index].axhline(q3, color='g', linestyle='--', label='q3')
            # 將最大值添加到列表中
        max_values.append(max_val)
        ax[index].annotate("max: {:.2f}".format(max_val), xy=(0, max_val), xytext=(0, max_val+0.1), ha='right', color='red', fontsize=8, arrowprops=dict(facecolor='red', shrink=0.05))
        ax[index].annotate("max: {:.2f}".format(max_val), xy=(1, max_val), xytext=(1, max_val+0.1), ha='right', color='red', fontsize=8, arrowprops=dict(facecolor='red', shrink=0.05))
    # plt.tight_layout()
        ax[index].set_xlabel(name_list[index])
        ax[index].set_ylabel("")
    plt.show()
    
if __name__=="__main__":
    df= pd.read_csv("NFdata1415.csv")
    # name_list=['wbc','seg','band']
    # for i in name_list:
    #     print(df[i])
    drawImg(df)
