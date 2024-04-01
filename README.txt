Method Used:
    we will be getting the SMS data from Android Phone, 
    we will safe this 100 most recent raw messages in messages.db in messages_received table,

    The processed or extracted data is saved in round3.db in otp_data table.

    The database will be updated every 1 min for new messages.


Execution Steps:
    1) Connect Android Phone with USB Debugging ON.
    2) Run msg_data_extraction.py
    3) Run extraction.py
    4) Run app.py

