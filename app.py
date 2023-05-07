from distutils.command.config import config
from pickle import FALSE
from urllib import response
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,render_template_string,Blueprint
from flask_cors import CORS
import pymongo
from tools.jwtcreate import *
from tools.mongoDB import *
from tools.predict_NF import *
from tools.predict_sepsis import *
from tools.session import *
from tools.modelTraining import *
import tools.valueCouter 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import modelManage 

load_dotenv()
DATABASE_URL = 'mongodb+srv://admin:admin@personal.2p0d6yh.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(DATABASE_URL)
db = client.personalist
collection = db.user

# sercet_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for x in range(10))
sercet_key = 'u6IaMSFpafX_LVXCJZekenhIZ3KV9Ra1JA5vlDCkj'
UPLOAD_FOLDER='/uploadFile'
# app setting
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = sercet_key
app.config['PERMANENT_SESSION_LIFETIME'] = 60*60
app.config['SESSION_COOKIE_NAME'] = 'my_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
CORS(app)
app.register_blueprint(modelManage.modelManger)
@app.route('/', methods=['POST', 'GET'])
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        session['username'] = username
        result = password_check(collection, username, password)
        if result == None:
            return render_template('error.html', error_msg='帳號密碼錯誤！')
        token_fhir = createJWT_FHIR()
        token_user = createJWT_user(username=username)
        session['username'] = username
        session['token_fhir'] = token_fhir
        session['token_user'] = token_user
        token_update(collection, username, token_fhir, token_user)
        response = redirect(url_for('patientlist'))
        return response

@app.route('/patientlist')
def patientlist():
    template_name = 'patientlist.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/patientprofile')
def patientprofile():
    template_name = 'patientprofile.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/NFchoice')
def NFchoice():
    template_name = 'NFchoice.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/NF')
def NF():
    template_name = 'NF.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/sepsischoice')
def sepsischoice():
    template_name = 'sepsischoice.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/sepsis')
def sepsis():
    template_name = 'sepsis.html'
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user):
        return render_template(template_name)
    return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

@app.route('/mapping')
def mapping():
    return render_template('mapping.html')

@app.route('/GET/token_fhir', methods=['GET'])
def token_fhir():
    username = getsession(session, 'username')
    token_user = getsession(session, 'token_user')
    token_fhir = getsession(session, 'token_fhir')
    if usertoken_check(collection, username, token_user) == None:
        return render_template('error.html', error_msg='使用者未登入！[MongoDBtokenError]')
    print('usertoken_check succeeded')
    if verifyJWT_user(username, token_user) == False:
        return render_template('error.html', error_msg='使用者未登入！[SessionTokenError]')

    return jsonify(token_fhir)


@app.route('/GET/predict/NF', methods=['POST'])
def predict_NF():
    if request.method == 'POST':
        try:
            insertdata = request.get_json()
        except:
            insertdata={'sea':float(request.values['sea']),
                        'wbc':float(request.form['wbc']),
                        'crp':float(request.form['crp']),
                        'seg':float(request.form['seg']),
                        'band':float(request.form['band']),
                        }
        result = NFPredict(insertdata['sea'], insertdata['wbc'],
                           insertdata['crp'], insertdata['seg'], insertdata['band'])
        new_result = {
            'decisionTree': str(result['decisionTree']),
            'randomForest': str(result['randomForest']),
            'logisticregression': str(result['logisticregression']),
            'neuralNetwork': str(result['neuralNetwork']),
            'supportVectorMachine': str(result['supportVectorMachine']),
            'decisionTree_proba': str(result['decisionTree_proba']),
            'randomForest_proba': str(result['randomForest_proba']),
            'logisticregression_proba': str(result['logisticregression_proba']),
            'neuralNetwork_proba': str(result['neuralNetwork_proba']),
            'supportVectorMachine_proba': str(result['supportVectorMachine_proba'])
        }
        print(insertdata)
        print(new_result)
        return jsonify(new_result)


@app.route('/GET/predict/sepsis', methods=['POST'])
def predict_sepsis():
    if request.method == 'POST':
        insertdata = request.get_json()
        result = sepsisPredict(insertdata['gcs'], insertdata['meds_ams15b'], insertdata['meds_plt150b'], insertdata['sofa_res'], insertdata['sofa_ner'], insertdata['sofa_liver'], insertdata[
            'sofa_coag'], insertdata['sofa_renal'], insertdata['bun'], insertdata['cre'], insertdata['plt'], insertdata['FIO2_percent'], insertdata['PF_ratio'], insertdata['fio2_per'], insertdata['fio2_cb'])
        new_result = {
            'randomForest': str(result['randomForest']),
            'logisticregression': str(result['logisticregression']),
            'supportVectorMachine': str(result['supportVectorMachine']),
            'randomForest_proba': str(result['randomForest_proba']),
            'logisticregression_proba': str(result['logisticregression_proba']),
            'supportVectorMachine_proba': str(result['supportVectorMachine_proba'])
        }
        print(insertdata)
        print(new_result)
        return jsonify(new_result)

@app.route('/realTimeNF', methods=['GET'])
def realTimeNF():
    return render_template('realTimePredict_NF.html')

@app.route('/realTimeSpesis', methods=['GET'])
def realTimeSpesis():
    return render_template('realTimePredict_spesis.html')

@app.route('/addPatient',methods=['GET'])
def addPatient():
    return render_template('addPatient.html')

@app.route('/edit')
def edit():
     return render_template('patientBodyData_NF.html')

@app.route('/singlePlot',methods=['get'])
def get_singlePlot():
    df = pd.read_csv('危險因子分析/Fdata1415.csv')
    df2=pd.read_csv('危險因子分析/Fdata1415.csv')
    df.drop('nf',axis=1,inplace=True)
    l=['wbc','crp','seg','band']
    headers=list(df.columns)
    for i in headers:
        if i not in l:
            df.drop(i,axis=1,inplace=True)
    return render_template('analyze_single.html', columns=df.columns,img="",choose="",pvalue=tools.valueCouter.p_value(df2))
@app.route('/singlePlot',methods=['post'])
def singlePlot():
    df_ori = pd.read_csv('危險因子分析/Fdata1415.csv')
   # column_headers = list(df_ori.columns)
    max_values=[]
    name_list=[request.form.get('y'),request.form.get('y')]
    
    fig = plt.figure(figsize=(16, 9))
    
    ax = fig.subplots(1, 2)
    # mgr = plt.get_current_fig_manager()

    # 切換至全螢幕模式
    # mgr.full_screen_toggle()        
    for index,i in enumerate(name_list):
        # column_headers=df[i]
        df=df_ori[df_ori['nf']==index%2]
        df.sort_values(by=name_list[index])
        

        sns.boxplot(x='nf', y=i, data=df,ax=ax[index],palette=['#9ee4e8','#0000FF'])
        #change boxplot color
        
        #ax[index].set_xticklabels(['NF', 'Sepsis'])

        #ax[index].tick_params(axis='x', labelleft=False, labelright=True)
        q1, q2, q3 = df[i].quantile(q=[0.25, 0.5, 0.75])
        max_val=df[i].max()
        # 繪製平均值、中位數和四分位數
        ax[index].axhline(df[i].mean(), color='r', linestyle='--', label='mean')
        ax[index].annotate("mean: {:.2f}".format(df[i].mean()), xy=(-0.5, df[i].mean()), xytext=(-0.5, df[i].mean()), ha='right', color='red', fontsize=8)
        # ax[index].axhline(q1, color='g', linestyle='--', label='q1')
        # ax[index].axhline(q2, color='b', linestyle='--', label='q2')
        # ax[index].axhline(q3, color='g', linestyle='--', label='q3')
        ax[index].annotate("25%: {:.2f}".format(q1), xy=(0.5, q1), xytext=(0.65, q1), ha='right', color='green', fontsize=8)
        ax[index].annotate("50%: {:.2f}".format(q2), xy=(0.5, q2), xytext=(0.65,q2), ha='right', color='blue', fontsize=8)
        ax[index].annotate("75%: {:.2f}".format(q3), xy=(0.5, q3), xytext=(0.65, q3), ha='right', color='green', fontsize=8)
        
        
            # 將最大值添加到列表中
        max_values.append(max_val)
        
        largest_values = df.nlargest(5, name_list[index])[name_list[index]].tolist()
        for max_index,max_val in enumerate(largest_values):
            f=lambda x: 'left' if x else 'right'
            ax[index].annotate("the {}  : {:.2f}".format(max_index+1,max_val), xy=(0, max_val), xytext=(0, max_val+0.1), ha=f(max_index%2), color='red' , fontsize=8 )
            ax[index].annotate("the {}  : {:.2f}".format(max_index+1,max_val), xy=(1, max_val), xytext=(1, max_val+0.1), ha=f(max_index%2), color='red', fontsize=8)
    # plt.tight_layout()
        ax[index].set_xlabel(name_list[index]+" when nf is "+str(index%2==0))
        ax[index].set_ylabel("")
    fig=fig.get_figure()
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode()
    l=['wbc','crp','seg','band']
    headers=list(df.columns)
    for i in headers:
        if i not in l:
            df.drop(i,axis=1,inplace=True)
    return render_template('analyze_single.html', columns=df.columns,img=graphic,choose=["nf",request.form.get('y')],pvalue=tools.valueCouter.p_value(df_ori))

@app.route('/plot',methods=['get'])
def before_plot():
    df = pd.read_csv('危險因子分析/NFdata1415.csv')
    # df.drop('ID',axis=1,inplace=True)
    l=['nf','wbc','crp','seg','band']
    headers=list(df.columns)
    for i in headers:
        if i not in l:
            df.drop(i,axis=1,inplace=True)
    # 傳遞參數到 HTML 畫面
    return render_template('analyze_double.html', columns=df.columns,img="",choose="",pvalue=tools.valueCouter.p_value(df))
@app.route('/plot',methods=['post'])
def plot():
    # 從 request 取得使用者選擇的參數
    df = pd.read_csv('危險因子分析/NFdata1415.csv')
    # df.drop('ID',axis=1,inplace=True)
    l=['nf','wbc','crp','seg','band']
    headers=list(df.columns)
    for i in headers:
        if i not in l:
            df.drop(i,axis=1,inplace=True)
    x_col = request.form.get('x')
    y_col = request.form.get('y')
    choose=[x_col,y_col]
    # 產生散佈圖
    plot_data = df[[x_col, y_col]].dropna()
    #if nf=1 set to red
    plot_data['nf']=df['nf']
    plot_data['nf']=plot_data['nf'].apply(lambda x: 'red' if x else 'green')

    fig = plot_data.plot.scatter(x=x_col, y=y_col,c='nf').get_figure()
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode()
    # 傳回圖片
    # html = '''
    #     <div>
    #         <img src="data:image/png;base64,{}">
    #     </div>
    # '''
    return render_template('analyze_double.html',columns=df.columns,img=graphic,choose=choose,pvalue=tools.valueCouter.p_value(df))
@app.route('/upload',methods=['GET','POST'])
def uploadCSV():
    if request.method == 'POST':
        print("POST")
        # 檢查是否有上傳檔案
        for i in request.files:
            print(i)
        if 'file' not in request.files:
            return '沒有上傳檔案'
        
        # 取得上傳的檔案
        #print(request.files)
        file = request.files['file']
        #print("GET FILE")
        # 檢查檔案是否符合條件
        if file.filename == '':
            return '沒有選擇檔案'
        
        # 讀取 CSV 檔案
        df = pd.read_csv(file)
        
        try:
            print("SUCCESS")
            training(df=df)
            
        except Exception as e:
            return "500 internal error"
        return render_template("upload.html",success=True)
        # 將檔案內容印出來
    return render_template("upload.html",success=False)
if __name__ == '__main__':
    app.run("localhost",5001,debug=True)
