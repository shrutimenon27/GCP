import numpy as np
from flask import Flask, request, render_template
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])

def predict():


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
        #a = ((a - 0.08) / (82 - 0.08))

        # hyper-tension
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

        # worktype
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

        # residency-type
        residency = request.form['residency']
        residency = residency.lower()
        if residency == "urban":
            residency = 1
        else:
            residency = 0

        # glucose-levels
        glucose = request.form['glucose']
        glucose = int(glucose)

        # bmi
        bmi = request.form['bmi']
        bmi = int(bmi)

        # smoking
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
        input = [gender, age, hypertension, heart_disease, marriage, worktype, residency, glucose, bmi, smoking]
        minimum = [ 0, 0.08, 0, 0, 0, 0, 0, 55.12, 10.3, 0]
        maximum = [2, 82, 1, 1, 1, 4, 1, 271.74, 97.6, 3]
        minimum = np.array(minimum)
        maximum = np.array(maximum)
        input_scaled = (input - minimum) / (maximum - minimum)

        try:
            # predictions
            result = model.predict([input_scaled])
        
            # output
            if result[0] == 1:
                output = 'Person has chances of Having Stroke'
            else:
                output = 'Person has no risk of Stroke'
             
            return render_template('home.html', prediction_text=output)


        except ValueError:
            return "Please Enter Valid Values"



if __name__ == "__main__":
    app.run(debug = True)
