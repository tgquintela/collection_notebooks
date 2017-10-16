
import sys
import os
import argparse
import datetime

from ts_tools import get_blood_std_48h, read_motion, read_blood_glucose
from sklearn.externals import joblib


def process_line_data(line_data):
    line_data = line_data.strip()
#    data = line_data.split('\t')
    try:
        data = line_data.split('\t')
        assert(len(data) == 6)
    except:
        try:
            data = line_data.replace('\t', ' ')
            data = line_data.split(' ')
            assert(len(data) == 6)
        except:
            data = line_data.split(' ')
            assert(len(data) == 6)
    assert(len(data) == 6)
    return data


def predict_proba_interval(data):
    model = joblib.load('model_interval_blood_glucose.pkl')    
    return model.predict_proba(float(data[1]))[0][0]*100


def predict_proba_48h(data):
    model = joblib.load('model_blood_glucose.pkl')
    dtime = datetime.datetime.strptime(data[0], '%Y-%m-%dT%H:%M:%S.%f+00:00')

    blood_glucose = read_blood_glucose()
    motion = read_motion()
    get_blood_std_48h(dtime, motion, blood_glucose)

    return model.predict_proba(float(data[1]))[0][0]*100


def predict_proba(data, mode='interval'):
    if mode == 'interval':
        return predict_proba_interval(data)
    else:
        return predict_proba_48h(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Process mode of prediction")
    parser.add_argument('--mode', type=str, action="store", default="interval",
                        help="mode of prediction (default: interval)")
    pos_args = parser.parse_args(sys.argv[1:])
    mode = pos_args.mode

    for line_data in sys.stdin:
        if line_data.strip() == 'exit':
            break
        data = process_line_data(line_data)
        pred = predict_proba(data, mode)
        print("Probabilty of high variance of blood glucose: {}%".format(pred))
