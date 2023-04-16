import pickle
import pandas as pd
import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Dropout
import tensorflow as tf
from tensorflow.keras.models import load_model
randomForest_mean = {'sea': 2.64367816e-01, 'wbc': 1.29186782e+04,
                     'crp': 1.02275316e+02, 'seg': 7.77652299e+01, 'band': 2.15287356e+00}
randomForest_std = {'sea': 4.40996002e-01, 'wbc': 6.87577970e+03,
                    'crp': 1.04717608e+02, 'seg': 1.03838581e+01, 'band': 5.10361803e+00}
logisticregression_mean = {'sea': 2.67241379e-01, 'wbc': 1.26043103e+04,
                           'crp': 9.81396264e+01, 'seg': 7.74643678e+01, 'band': 2.22183908e+00}
logisticregression_std = {'sea': 4.42519406e-01, 'wbc': 6.73628951e+03,
                          'crp': 1.02613321e+02, 'seg': 1.13604398e+01, 'band': 5.16601795e+00}
neuralNetwork_mean = {'sea': 0.267241, 'wbc': 12802.873563,
                      'crp': 99.245230, 'seg': 76.881322, 'band': 2.165805}
neuralNetwork_std = {'sea': 0.443157, 'wbc': 6733.317976,
                     'crp': 100.752599, 'seg': 11.649307, 'band': 5.155407}
supportVectorMachine_mean = {
    'sea': 2.64367816e-01, 'wbc': 1.28008621e+04, 'crp': 9.90701552e+01, 'seg': 7.73261494e+01, 'band': 2.13017241e+00}
supportVectorMachine_std = {'sea': 4.40996002e-01, 'wbc': 7.00600927e+03,
                            'crp': 1.08474071e+02, 'seg': 1.05109073e+01, 'band': 5.10247663e+00}


def NFPredict(sea, wbc, crp, seg, band):
    pred = {}
    randomForest_transform = {'sea': ((sea - randomForest_mean['sea']) / randomForest_std['sea']),
                              'wbc': ((wbc - randomForest_mean['wbc']) / randomForest_std['wbc']),
                              'crp': ((crp - randomForest_mean['crp']) / randomForest_std['crp']),
                              'seg': ((seg - randomForest_mean['seg']) / randomForest_std['seg']),
                              'band': ((band - randomForest_mean['band']) / randomForest_std['band'])}
    logisticregression_transform = {'sea': ((sea - logisticregression_mean['sea']) / logisticregression_std['sea']),
                                    'wbc': ((wbc - logisticregression_mean['wbc']) / logisticregression_std['wbc']),
                                    'crp': ((crp - logisticregression_mean['crp']) / logisticregression_std['crp']),
                                    'seg': ((seg - logisticregression_mean['seg']) / logisticregression_std['seg']),
                                    'band': ((band - logisticregression_mean['band']) / logisticregression_std['band'])}
    neuralNetwork_transform = {'sea': ((sea - neuralNetwork_mean['sea']) / neuralNetwork_std['sea']),
                               'wbc': ((wbc - neuralNetwork_mean['wbc']) / neuralNetwork_std['wbc']),
                               'crp': ((crp - neuralNetwork_mean['crp']) / neuralNetwork_std['crp']),
                               'seg': ((seg - neuralNetwork_mean['seg']) / neuralNetwork_std['seg']),
                               'band': ((band - neuralNetwork_mean['band']) / neuralNetwork_std['band'])}
    supportVectorMachine_transform = {'sea': ((sea - supportVectorMachine_mean['sea']) / supportVectorMachine_std['sea']),
                                      'wbc': ((wbc - supportVectorMachine_mean['wbc']) / supportVectorMachine_std['wbc']),
                                      'crp': ((crp - supportVectorMachine_mean['crp']) / supportVectorMachine_std['crp']),
                                      'seg': ((seg - supportVectorMachine_mean['seg']) / supportVectorMachine_std['seg']),
                                      'band': ((band - supportVectorMachine_mean['band']) / supportVectorMachine_std['band'])}

    # decisionTree
    model_file_name = 'static/model/NF_decisionTree.pickle'
    with open(model_file_name, 'rb') as f:
        model1 = pickle.load(f)
        score1 = model1.predict_proba(
            np.array([[sea, wbc, crp, seg, band]]))[0]
    if (score1[0] > 0.5):
        pred['decisionTree_proba'] = np.round(score1[0]*100, 2)
        pred['decisionTree'] = 0
    else:
        pred['decisionTree_proba'] = np.round(score1[1]*100, 2)
        pred['decisionTree'] = 1

    # randomForest
    model_file_name = 'static/model/NF_randomForest.pickle'
    with open(model_file_name, 'rb') as f:
        model2 = pickle.load(f)
        score2 = model2.predict_proba(
            np.array([[randomForest_transform['sea'], randomForest_transform['wbc'], randomForest_transform['crp'], randomForest_transform['seg'], randomForest_transform['band']]]))[0]
    if (score2[0] > 0.5):
        pred['randomForest_proba'] = np.round(score2[0]*100, 2)
        pred['randomForest'] = 0
    else:
        pred['randomForest_proba'] = np.round(score2[1]*100, 2)
        pred['randomForest'] = 1

    # logisticregression
    model_file_name = 'static/model/NF_logisticregression.pickle'
    with open(model_file_name, 'rb') as f:
        model3 = pickle.load(f)
        score3 = model3.predict_proba(np.array(
            [[logisticregression_transform['sea'], logisticregression_transform['wbc'], logisticregression_transform['crp'], logisticregression_transform['seg'], logisticregression_transform['band']]]))[0]
    if (score3[0] > 0.5):
        pred['logisticregression_proba'] = np.round(score3[0]*100, 2)
        pred['logisticregression'] = 0
    else:
        pred['logisticregression_proba'] = np.round(score3[1]*100, 2)
        pred['logisticregression'] = 1

    # neuralNetwork
    # model_file_name = 'static/model/NF_neuralNetwork.pickle'
    # # with tf.device('/job:localhost'):
    # #     model4 = tf.keras.models.load_model(model_file_name)
    # with open(model_file_name, 'rb') as f:
    model4 = load_model('static/model/NF_neuralNetwork.h5')
    pred4 = model4.predict(np.array(
        [[neuralNetwork_transform['sea'], neuralNetwork_transform['wbc'], neuralNetwork_transform['crp'], neuralNetwork_transform['seg'], neuralNetwork_transform['band']]]))
    pred4 = pred4[0][0]
    if (pred4 > 0.5):
        pred['neuralNetwork'] = 1
        pred['neuralNetwork_proba'] = np.round(pred4*100, 2)
    else:
        pred['neuralNetwork'] = 0
        pred['neuralNetwork_proba'] = 100 - np.round(pred4*100, 2)

    # supportVectorMachine
    model_file_name = 'static/model/NF_supportVectorMachine.pickle'
    with open(model_file_name, 'rb') as f:
        model5 = pickle.load(f)
        score5 = model5.predict_proba(np.array(
            [[supportVectorMachine_transform['sea'], supportVectorMachine_transform['wbc'], supportVectorMachine_transform['crp'], supportVectorMachine_transform['seg'], supportVectorMachine_transform['band']]]))[0]
    if (score5[0] > 0.5):
        pred['supportVectorMachine_proba'] = np.round(score5[0]*100, 2)
        pred['supportVectorMachine'] = 0
    else:
        pred['supportVectorMachine_proba'] = np.round(score5[1]*100, 2)
        pred['supportVectorMachine'] = 1

    return pred
