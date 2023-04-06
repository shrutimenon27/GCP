# Stroke-Prediction1

To run the app in local environment:

1. Open Terminal on Computer
2. Perform git clone of the repository 
3. Execute the following:
export FLASK_APP=app.py 
flask run
4. Run in browser: http://127.0.0.1:5000

To run the app on google app engine:

1. Open Activate CloudShell, change current directory to project dir then Run:
python3 -m venv env
source env/bin/activate
2. pip install -r requirements.txt
3. gcloud app deploy
4. Run URL in browser
