from flask import Flask, render_template, request
from extraction import data_fetch,databaseInit
from msg_data_extraction import update_db
import threading 
import time
import schedule


app = Flask(__name__)

def run_code():
    while True:

        update_db()
        databaseInit(update=True)

        time.sleep(60)

def background_thread():
    schedule.every(1).minute.do(run_code)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/',methods=['GET','POST'])

def index():
    data  = data_fetch()
    print(data)
    return render_template('index.html',message=data[1],data = data[2:])
    

if __name__ == '__main__':

    thread = threading.Thread(target = background_thread)
    thread.start()

    app.run(debug=True)