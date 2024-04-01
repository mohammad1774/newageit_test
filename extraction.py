import re
from datetime import datetime as dt
import sqlite3
from fuzzywuzzy import fuzz
import pickle

def database_conn():
    conn = sqlite3.connect('round3.db')
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS otp_data (id INTEGER PRIMARY KEY,
                message TEXT NOT NULL,
                otp TEXT NOT NULL,
                time TEXT NOT NULL,
                website TEXT NOT NULL)''')
    
    conn.commit()
    cursor.close()
    conn.close()


def data_input(data):

    conn = sqlite3.connect('round3.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO otp_data (message, otp, time, website) VALUES (?,?,?,?)',
                   (data['message'],data['otp'],data['time'],data['website']))
    

    conn.commit()
    cursor.close()
    conn.close()


def data_fetch():

    conn = sqlite3.connect('round3.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM otp_data ORDER BY id DESC LIMIT 1')

    recent_row = cursor.fetchone()

    #print('last row', recent_row)

    cursor.close()
    conn.close()
    return recent_row


def website_extraction(row):
    sms = row[1]
    backup_website = row[-1]

    with open('company_names.pkl','rb') as file:
        company_names = pickle.load(file)

    for word in sms.split():
        for company in company_names:
            if fuzz.partial_ratio(word.lower(), company.lower()) >= 50:
                return company
    
    return backup_website



def otp_extraction(row):
    data = {}
    sms = row[1]
    data['message'] = sms
    data['time'] = row[2]


    structure_otp = re.compile(r'\b\d{4,6}\b')
    match_otp = structure_otp.search(sms)    
    if match_otp:
        print(f'match found:{match_otp.group}')
        data['otp'] = match_otp.group()
    else:
        print('match not found')
        data['otp'] = None


    data['website'] = website_extraction(row)

    if data['otp'] != None:
        database_conn()
        data_input(data)


def databaseInit(update = False):

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages_received')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if update == False:
        for row in data:
            print(row[1])
            otp_extraction(row)
    else:
        print(data[-1][1])
        otp_extraction(data[-1])

databaseInit()
        
#print(data_fetch())