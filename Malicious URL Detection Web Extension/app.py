from flask import Flask, request, jsonify
from urllib.parse import urlparse
import joblib
from feature_extraction import extract_features
from flask_cors import CORS
import pandas as pd
import os

#Create a Flask app instance
app = Flask(__name__)
CORS(app)

#Load models and lists from config file
from config import rf_model_path, lr_model_path, xgb_model_path, WHITELIST_FILE, BLACKLIST_FILE
rf_model = joblib.load(rf_model_path)
lr_model = joblib.load(lr_model_path)
xgb_model = joblib.load(xgb_model_path)

#Function to update whitelist/blacklist
def update_list(file_path, domain, add=True):
    with open(file_path, 'r+') as file:
        lines = set(file.read().splitlines())
        file.seek(0)
        file.writelines(f"{line}\n" for line in (lines | {domain} if add else lines - {domain}))
        file.truncate()

#Function to read whitelist/blacklist
def read_list(file_path):
    return open(file_path, 'r').read().splitlines() if os.path.exists(file_path) else []

#Route to update the whitelist
@app.route('/update_whitelist', methods=['POST'])
def update_whitelist():
    update_list(WHITELIST_FILE, request.json['url'], request.json['add'])
    return jsonify({'message': 'Whitelist updated'})

#Route to update the blacklist
@app.route('/update_blacklist', methods=['POST'])
def update_blacklist():
    update_list(BLACKLIST_FILE, request.json['url'], request.json['add'])
    return jsonify({'message': 'Blacklist updated'})

#Route to get the blacklist and whitelist 
@app.route('/get_lists', methods=['GET'])
def get_lists():
    return jsonify({'whitelist': read_list(WHITELIST_FILE), 'blacklist': read_list(BLACKLIST_FILE)})

#Route to analyze and categorize URL
@app.route('/check_url', methods=['POST'])
def check_url():
    try:
        url = request.json['url']
        #Check if the URL is in the whitelist
        if any(urlparse(url).netloc in item for item in read_list(WHITELIST_FILE)):
            return jsonify({'Result': 'Whitelisted'})
        #Check if the URL is in the blacklist
        if any(urlparse(url).netloc in item for item in read_list(BLACKLIST_FILE)):
            return jsonify({'Result': 'Blacklisted'})

        #Extracting features from the URL and create a dataframe
        features_df = pd.DataFrame([extract_features(url)], columns=[
            'count_specialchar', 'count_sensitive_words', 'using_shortener', 'has_at_symbol', 'count_double_slash', 'count_dash_symbol',
            'count_multiple_subdomains', 'url_length', 'https', 'contains_ip_address', 'url_entropy', 'numchar_classification'])
        
        #Model prediction and returning the results
        return jsonify({ 'Random Forest': 'Malicious' if rf_model.predict(features_df)[0] == 1 else 'Benign',
                         'Logistic Regression': 'Malicious' if lr_model.predict(features_df)[0] == 1 else 'Benign',
                         'XGBoost': 'Malicious' if xgb_model.predict(features_df)[0] == 1 else 'Benign' })
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}', exc_info=True)
        return jsonify({'error': 'An error occurred during URL checking.'}), 500

#Running the flask app
if __name__ == '__main__':
    app.run(debug=True)
