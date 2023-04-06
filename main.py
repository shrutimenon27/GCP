import os
import logging
import json
#from google.cloud import secretmanager
from google.cloud import storage
import twilio
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from twilio import rest
from twilio.twiml import messaging_response
from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# create a client object to interact with the storage bucket
client = storage.Client()

# specify the bucket and file name of the model.pkl file
bucket_name = 'cloud-ai-platform-92295410-070a-449f-89d7-c6cd2ed9a7b1'
blob_name = 'model.pkl'

# get a reference to the bucket and blob objects
bucket = client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)

# download the model.pkl file from the storage bucket
model_bytes = blob.download_as_bytes()

# load the model.pkl file as a Python object
model = pickle.loads(model_bytes)


# Access the values by key
twilio_acct_sid = secrets['TWILIO_ACCT_SID']
auth_token = secrets['TWILIO_AUTH_TOKEN']
verify_sid = secrets['TWILIO_MSG_SID']

@app.route("/")
def index():
    return render_template('index.html')


def send_sms(phone_num, message):
    client = Client(twilio_acct_sid, auth_token)

    real_msg = client.messages.create(
        messaging_service_sid=verify_sid,
        body=message,
        to=phone_num
    )
    print(real_msg)


@app.route("/output", methods=["POST"])
# user-input
def output():
    if request.method == 'POST':

        # First Name
        first_name = request.form['firstname']

        # Last Name
        last_name = request.form['lastname']

        # gender
        gender = request.form['gender']
        if gender == "male":
            gender = 1
        elif gender == "female":
            gender = 0
        else:
            gender = 2

        # age
        age = request.form['age']
        age = int(age)

        # Hypertension
        hypertension = request.form['hypertension']
        hypertension = hypertension.lower()
        if hypertension == "yes":
            hypertension = 1
        else:
            hypertension = 0

        # heart-disease
        heart_disease = request.form['heart-disease']
        heart_disease = heart_disease.lower()
        if heart_disease == "yes":
            heart_disease = 1
        else:
            heart_disease = 0

        # marriage
        marriage = request.form['marriage']
        marriage = marriage.lower()
        if marriage == "yes":
            marriage = 1
        else:
            marriage = 0

        # Work-Type
        worktype = request.form['worktype']
        worktype = worktype.lower()
        if worktype == "government":
            worktype = 0
        elif worktype == "student":
            worktype = 1
        elif worktype == "private":
            worktype = 2
        elif worktype == "self-employed":
            worktype = 3
        else:
            worktype = 4

        # Residency-Type
        residency = request.form['residency']
        residency = residency.lower()
        if residency == "urban":
            residency = 1
        else:
            residency = 0

        # Glucose-Level
        glucose = request.form['glucose']
        glucose = int(glucose)

        # BMI
        bmi = request.form['bmi']
        bmi = int(bmi)

        # Smoking status
        smoking = request.form['smoking']
        if smoking == "unknown":
            smoking = 0
        elif smoking == "never smoked":
            smoking = 1
        elif smoking == "formerly smoked":
            smoking = 2
        elif smoking == "smokes":
            smoking = 3
        else:
            smoking = 0

        # Phone Number
        phone_num = request.form['phone']

        input = [gender, age, hypertension, heart_disease, marriage, worktype, residency, glucose, bmi, smoking]
        minimum = [0, 0.08, 0, 0, 0, 0, 0, 55.12, 10.3, 0]
        maximum = [2, 82, 1, 1, 1, 4, 1, 271.74, 97.6, 3]
        minimum = np.array(minimum)
        maximum = np.array(maximum)
        input_scaled = (input - minimum) / (maximum - minimum)

        try:
            result = model.predict([input_scaled])
            if result[0] == 1:
                pred = 'Person has chances of Having Stroke'

                send_sms(phone_num,
                         "Hello {} {}, You are at risk of stroke. Please consult your doctor immediately".format(
                             first_name, last_name))
            else:
                pred = 'Person has no risk of Stroke'
            return render_template('output.html', prediction=pred)

        except ValueError:
            return "Please Enter Valid Values"
        
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
