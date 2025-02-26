from flask import Flask, render_template, request, redirect
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Configure S3 client (IAM role will handle credentials on EC2)
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'your-s3-bucket-name'  # Replace with your bucket name

@app.route('/')
def index():
    try:
        # List files in S3 bucket
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', [])
        return render_template('index.html', files=objects)
    except NoCredentialsError:
        return "AWS credentials not configured!"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return redirect('/')

@app.route('/delete/<filename>')
def delete(filename):
    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
