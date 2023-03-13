import pickle
import pandas as pd
import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Dropout

mean = [1.39508929e+01, 4.15178571e-01, 8.30357143e-01, 9.86607143e-01, 4.62053571e-01, 2.34375000e-01, 4.39732143e-01,
        4.62053571e-01, 2.18155634e+01, 1.37572072e+00, 2.06002237e+02, 3.96549298e-01, 2.79831681e+02, 3.96549296e+01, 4.08576389e+01]
std = [2.45809506, 0.81116207, 1.34222891, 1.07728126, 0.9925559,  0.56376965, 0.81609475,
       0.91289731, 17.41744609, 1.61262408, 98.28342531, 0.12664999, 62.46864266, 12.66499879, 14.30293763]


def sepsisPredict(gcs, meds_ams15b, meds_plt150b, sofa_res, sofa_ner, sofa_liver,
                  sofa_coag, sofa_renal, bun, cre, plt, FIO2_percent, PF_ratio, fio2_per, fio2_cb):
    pred = {}
    transform = [gcs, meds_ams15b, meds_plt150b, sofa_res, sofa_ner, sofa_liver,
                 sofa_coag, sofa_renal, bun, cre, plt, FIO2_percent, PF_ratio, fio2_per, fio2_cb]
    print(transform)
    for i in range(0, 15):
        transform[i] = ((transform[i] - mean[i]) / std[i])
    print(transform)

    # randomForest
    model_file_name = 'tools/model/sepsis_randomForest.pickle'
    with open(model_file_name, 'rb') as f:
        model1 = pickle.load(f)
        pred1 = model1.predict(np.array([transform]))
        score1 = model1.predict_proba(
            np.array([transform]))[0]
    pred['randomForest'] = pred1[0]
    if (score1[0] > 0.5):
        pred['randomForest_proba'] = np.round(score1[0]*100, 2)
    else:
        pred['randomForest_proba'] = np.round(score1[1]*100, 2)

    # logisticregression
    model_file_name = 'tools/model/sepsis_logisticregression.pickle'
    with open(model_file_name, 'rb') as f:
        model2 = pickle.load(f)
        pred2 = model2.predict(np.array(
            [transform]))
        score2 = model2.predict_proba(np.array(
            [transform]))[0]
    pred['logisticregression'] = pred2[0]
    if (score2[0] > 0.5):
        pred['logisticregression_proba'] = np.round(score2[0]*100, 2)
    else:
        pred['logisticregression_proba'] = np.round(score2[1]*100, 2)

    # supportVectorMachine
    model_file_name = 'tools/model/sepsis_supportVectorMachine.pickle'
    with open(model_file_name, 'rb') as f:
        model3 = pickle.load(f)
        pred3 = model3.predict(np.array(
            [transform]))
        score3 = model3.predict_proba(np.array(
            [transform]))[0]
    pred['supportVectorMachine'] = pred3[0]
    if (score3[0] > 0.5):
        pred['supportVectorMachine_proba'] = np.round(score3[0]*100, 2)
    else:
        pred['supportVectorMachine_proba'] = np.round(score3[1]*100, 2)

    return pred
