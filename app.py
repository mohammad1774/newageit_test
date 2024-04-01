from flask import Flask, render_template, request
from extraction import *

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])

def index():
    if request.method == 'POST':
        message = request.form['message']
        processed_data = otp_extraction(message)  # Send message to processing file
        data = data_fetch()  # Fetch data from database using processing file
        return render_template('index.html', message=message, data=data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)