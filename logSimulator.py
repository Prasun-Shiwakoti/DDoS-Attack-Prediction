import pandas as pd
import random
import requests
import time
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime

# url of api endpoint
URL = 'http://127.0.0.1:5000/predict'

# number of request to send to server
turns = 10000

# to check for accuracy
y_true =  y_predict = []

# load dataset
df_simulate = pd.read_csv("Dataset/cicddos2019.csv")

# log printing function
def print_log(log_id, prediction, actualValue):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{current_time} - Log number: {log_id} : {actualValue}"

    if prediction == 1:
        log_message += "\n\t\t\t\t [ALERT: Potential Attack Detected]"

    # formatting the log message 
    print("-" * 120)
    print("\t" * 4, log_message)
    print("-" * 120)

# drop the unnecessary columns and encode the labels
df_simulate.drop('Label', axis=1, inplace=True)
df_simulate['Class'] = df_simulate['Class'].apply(lambda x: 1 if x=='Attack' else 0)

# make the simulation data
df_simulate_X = df_simulate.drop("Class", axis=1)
df_simulate_Y = df_simulate["Class"]


for i in range(turns):
    # randomly chooses which index to send to server
    ind = random.randrange(0, len(df_simulate_X))    

    data = df_simulate_X.iloc[ind].to_dict()

    # make the request
    response = requests.post(URL, json=data)

    model_prediction = response.json().get("prediction")
    if model_prediction is None:
        print(f"\nError: {response.json().get('error')}")
        continue
    actual_value = df_simulate_Y.iloc[ind]

    # add actual and predicted values to respective arrays
    y_true.append(actual_value)
    y_predict.append(model_prediction)

    # print the log
    print_log(ind, model_prediction, actual_value)
    time.sleep(1)

def calculate_accuracy(y_true, y_predict):
    # generates true negative, false positive, false negative and true positive data in matrix form
    conf_matrix = confusion_matrix(y_true, y_predict)

    accuracy = accuracy_score(y_true, y_predict)
    precision = precision_score(y_true, y_predict, average='binary', pos_label=1)
    recall = recall_score(y_true, y_predict, average='binary', pos_label=1)
    f1 = f1_score(y_true, y_predict, average='binary', pos_label=1)

    # Display the output
    print("\nAccuracy Metrics:")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print("\nConfusion Matrix:")
    print(conf_matrix)


calculate_accuracy(y_true, y_predict)
input()