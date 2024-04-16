"""
author: ben
reviewer:
"""

from flask import Flask, render_template, request, redirect, send_file
from weather import *
import socket
from botocore.exceptions import ClientError
import logging
import os

app = Flask(__name__)

env_gradient = os.environ.get('env_gradient')

logging.basicConfig(level=logging.INFO, filename="WeatherLogs.log",filemode="a", format="[%(asctime)s][%(levelname)s][%(message)s]")

city = None

user_selection = {}
@app.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'GET':

        logging.info(f"A user has entered the website")

        return render_template('index.html', method="get", socket=socket.gethostname(), env_gradient=env_gradient)
    
    if request.method == 'POST':
        global city

        city = request.form['city']

        data = get_weather_data(city)

        save_data_to_file(data)

        if data == "bad input":
            logging.warning(f"invalid city has been entered: {city}")
            return render_template('index.html',method="post", data=data)
        
        else:
            logging.info(f"city entered: {city}")
            return render_template('index.html',method="post", **get_weather_data(city))
        
    
@app.route("/health")
def health():
    return "ok"

@app.route("/download")
def download():
    try:
        return download_image()
    except ClientError as e:
        app.logger.error(f"S3 ClientError: {e}")
        return "Internal Server Error", 500
    
@app.route("/update-dynamodb", methods=['POST'])
def update_db():
    city = request.form['city']
    try:
        update_dynamodb(get_weather_data(city))
        return redirect('/')
    except ClientError as e:
        app.logger.error(f"S3 ClientError: {e}")
        return "Internal Server Error", 500
    
@app.route("/history")
def history():
    files = os.listdir('./Searches')
    # print(files)
    return render_template('DataDownload.html', files=files)

@app.route("/download-file/<filename>")
def download_file(filename):
    print(filename)
    return send_file(f'./Searches/{filename}', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)