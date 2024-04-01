import re
from datetime import datetime as dt
import sqlite3



# data = otp_extraction(sms='Flipkart: Use OTP 216127 to log in to your account. DO NOT SHARE this code with anyone, including the delivery executive. @www.flipkart.com #216127',time=dt.now())


# print(data)


def database_conn():
    conn = sqlite3.connect('round3.db')

    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS otp_data (id INTEGER PRIMARY KEY,
                otp TEXT NOT NULL,
                time TEXT NOT NULL,
                website TEXT NOT NULL)''')
    conn.commit()
    cursor.close()
    conn.close()


def data_input(data):

    conn = sqlite3.connect('round3.db')

    cursor = conn.cursor()

    cursor.execute('INSERT INTO otp_data (otp,time, website) VALUES (?,?,?)',
                   (data['otp'],data['time'],data['website']))
    

    conn.commit()
    cursor.close()
    conn.close()


def data_fetch():

    conn = sqlite3.connect('round3.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM otp_data ORDER BY id DESC LIMIT 1')

    recent_row = cursor.fetchone()

    print('last row', recent_row)

    cursor.close()
    conn.close()
    return recent_row


def otp_extraction(sms):
    time = dt.now()
    data = {}
    
    structure_otp = re.compile(r'\b\d{4,6}\b')

    match_otp = structure_otp.search(sms)
    
    if match_otp:
        print(f'match found:{match_otp.group}')
        #return match_otp.group()
        data['otp'] = match_otp.group()
        
    
    else:
        print('match not found')
        data['otp'] = None


    struct_website = re.compile(r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.[a-zA-Z]{2,}\b')

    match_web = struct_website.search(sms)

    #print(match_web)

    data['website']=match_web.group()

    data['time'] = time.strftime('%d/%m/%Y')

    #print(data)\

    database_conn()
    data_input(data)

    return data