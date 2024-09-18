from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import boto3
import config

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host=config.customhost,
    user=config.customuser,
    password=config.custompass,
    database=config.customdb
)
cursor = db.cursor()

# S3 Connection
s3 = boto3.client('s3', 
                  aws_access_key_id=config.customuser,
                  aws_secret_access_key=config.custompass,
                  region_name=config.customregion)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    purpose = request.form['purpose']
    brand = request.form['brand']
    model = request.form['model']
    city = request.form['city']
    branch = request.form['branch']
    mobile_number = request.form['mobile_number']
    
    # Store data in MySQL
    sql = "INSERT INTO visitors (purpose, brand, model, city, branch, mobile_number) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (purpose, brand, model, city, branch, mobile_number)
    cursor.execute(sql, values)
    db.commit()

    # Store data in S3
    visitor_data = f"Purpose: {purpose}, Brand: {brand}, Model: {model}, City: {city}, Branch: {branch}, Mobile: {mobile_number}"
    s3.put_object(Bucket=config.custombucket, Key=f"visitor_{mobile_number}.txt", Body=visitor_data)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
