from flask import *
from jinja2 import Environment, FileSystemLoader

import boto3
import csv
import pandas as pd
import json

app = Flask(__name__)
from werkzeug.utils import secure_filename

# import key_config as keys

s3 = boto3.client('s3',
                  aws_access_key_id='AKIAVBROUFH5RFFCXM3C',
                  aws_secret_access_key='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'
                  )

lambda_client = boto3.client('lambda',
                             aws_access_key_id='AKIAVBROUFH54FYOL4ZE',
                             aws_secret_access_key='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'
                             )
# s3 = boto3.client('s3')
BUCKET_NAME = 'naveen1-bucket'
LAMBDA_NAME = 'demo-lambda'

@app.route('/')
def home():
    return render_template("html1.html")

data2=[]
@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['csvfile']
        if img: 
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            ) 
            msg = "Upload Done ! "
            
            data=[]
            with open(filename) as file:
                csvfile = csv.reader(file)
                for row in csvfile:
                    data.append(row)
                    data2.append(row)
            data = pd.DataFrame(data)
            
            if data.shape[0]>100:
                #return render_template("html1.html", msg=msg)
                if request.method == 'POST':
                    return redirect(url_for('adding'))
            else:
                json_string = data.to_json()
                #payload = {'data': json_string}



                response = lambda_client.invoke(
                    FunctionName=LAMBDA_NAME,
                    Payload=str(json_string))
                response_payload = response['Payload'].read()
                print(response_payload.decode('utf-8'))
                return 'Go to lambda'
            
@app.route('/adding', methods=['GET','POST'])
def adding():
    if request.method == 'POST':
        data = pd.DataFrame(data2)
        return render_template_string('''{{ data | safe }} <html>
        <h1>USER ADDING DETAIL FORM</h1>
        <body>
        <form method="POST">
        First_value :<input name="first-value">
        <br/><br/>
        Second_value :<input name="second-value">
        <br/><br/>
        Third_value : <input name="third-value">
        <br/><br/>
        Fourth_value : <input name="fourth-value">
        <br/><br/>
        <button type="submit">Submit</button>
        </form>
        </body>
        </html>''',data=data.to_html(header=False))



if __name__ == "__main__":
    app.run(debug=True)

