from distutils.command.config import config
from pickle import FALSE
from urllib import response
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import pymongo
from tools.jwtcreate import *
from tools.mongoDB import *
from tools.predict_NF import *
from tools.predict_sepsis import *
from tools.session import *

load_dotenv()
DATABASE_URL = 'mongodb+srv://admin:admin@personal.2p0d6yh.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(DATABASE_URL)
db = client.personalist
collection = db.user

# sercet_key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for x in range(10))
sercet_key = 'u6IaMSFpafX_LVXCJZekenhIZ3KV9Ra1JA5vlDCkj'

# app setting
app = Flask(__name__)
app.config['SECRET_KEY'] = sercet_key
app.config['PERMANENT_SESSION_LIFETIME'] = 60*60
app.config['SESSION_COOKIE_NAME'] = 'my_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)


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

# value api


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
        insertdata = request.get_json()
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


if __name__ == '__main__':
    app.run(debug=True)
