import subprocess
import sqlite3
import re
import datetime


def get_sms_data():
    result = subprocess.run(["adb", "shell", "content", "query", "--uri", "content://sms"], 
                            capture_output=True, text=True,encoding='utf-8')
    
    if result.returncode == 0:
        sms_data = result.stdout
        return sms_data
    else:
        print("Error retrieving SMS data.")
        return None


def domain_extraction(msg):
    struct_website = re.compile(r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)\.[a-zA-Z]{2,}\b')
    match_web = struct_website.search(msg)
    if match_web:
        return match_web.group()
    
    else:
        return None


def database_init():
    conn = sqlite3.connect('messages.db')

    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS messages_received (id INTEGER PRIMARY KEY,
                message TEXT,
                time TEXT,
                website TEXT)''')
    conn.commit()
    cursor.close()
    conn.close()


def extract_rows(data, update = False):

    sms_list = data.strip().split("Row: ")[1:]
    
    if update:
        update_db_row(sms_list[0])
    else:
        for sms in sms_list[:100]:
            update_db_row(sms)
    

def update_db_row(sms):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    
    fields = sms.strip().split(", ")
    print(sms)
    body = None
    date = None
    for field in fields:
        if field.startswith("body="):
            body = field.split("body=")[1]
            website = domain_extraction(body)
        if field.startswith("date_sent="):
            time = int(field.split('date_sent=')[1])
            print(time)
            dt_object = datetime.datetime.fromtimestamp(time / 1000)

            date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            print(date)
                
    cursor.execute('INSERT INTO messages_received (message, time, website) VALUES (?,?,?)',
                        (body,date,website))
            
    conn.commit()
    cursor.close()
    conn.close()
    
    
def update_db():
    sms_data = get_sms_data()
    extract_rows(sms_data,update=True)
    

if __name__ == "__main__":
    sms_data = get_sms_data()
    database_init()
    extract_rows(sms_data)

    if sms_data:
        print("""The data is stored in the messages.db database with table messages_received table where column names are 
               Id , Message, Time , Website Name.""")
        #print(type(sms_data))