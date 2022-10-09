

from lambda_function import lambda_handler

from flask import Flask,render_template,request
import logging
from templates import *
import os
import shutil
from helper import checker


import json
from constants import IMAGE_FOLDER, PDF_NAME,ROOT
from pathlib import Path



app = Flask(__name__)






@app.route('/')
def hello():
   
    return render_template('success.html')

# @app.route('/remove' , methods = ['DELETE'])
# def remove():
#     client = boto3.client('s3',aws_access_key_id= AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY,region_name= REGION_NAME)
    
#     client.delete_object(Bucket = BUCKET, Key = PDF_NAME )
#     headers = {
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Headers': 'Content-Type',
#             'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
#         }
#     response = {
#         'statusCode': 200,
#         'body': json.dumps('response_data'),
#         'headers': headers
#     }
#     return response
@app.route('/home', methods=['GET','POST'])
def home():
    
    
    if request.method == 'POST' and len(request.files.getlist('img')) > 0:
        checker(os.path.join(ROOT,IMAGE_FOLDER))
        images = request.files.getlist('img')

        
        for i in range(len(images)):
            name = images[i].filename

            image_path = os.path.join(ROOT,IMAGE_FOLDER)

            images[i].save(os.path.join(image_path,name))
        response,name = lambda_handler()
        if response == True:
            
            return render_template('pdf_done.html',value = [PDF_NAME])
        else:
            
            return f'<h1> {name} </h1>'

    return render_template('image_input.html')

if __name__ == '__main__':
    app.run()
    
    
    logging.basicConfig(filename='record.log', level=logging.DEBUG)