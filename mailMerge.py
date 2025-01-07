from csv import DictReader
from smtplib import SMTP
from os.path import join
from email.message import EmailMessage
from email.mime.text import MIMEText



# Credentials
SENDER_EMAIL = input('Sender Email: ')
SENDER_PASSWORD = input('App Password: ')

# Fields
FROM = input('From: ')
SUBJECT = input('Subject: ')

# Name of the email body (HTML or plain text only)
BODY_FILENAME = input('Body Filename: ')
BODY_FILENAME = join('.',BODY_FILENAME)

# CSV database
DATABASE_FILENAME = input('CSV Filename: ')
DATABASE_FILENAME = join('.',DATABASE_FILENAME)



# SMTP server DO NOT CHANGE
SERVER = SMTP("smtp.gmail.com", 587)



# Initializes user
def initEmailService():
    try:
        SERVER.starttls()
        SERVER.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Logged in")
    except:
        print("Error when logging in. Please check your user email and password.")
        quit()

# Constructs body of the email message from an html file
def constructBody(fields, contact):
    try:
        with open(BODY_FILENAME, 'r', encoding="utf-8") as file:
            body = ''.join(file.readlines())
            body = body.replace("[ sign off ]", FROM)
            for field in fields:
                body = body.replace(f"[{field}]", contact[field])
            file.close()
        return MIMEText(body, 'html')
    except:
        print("Error with the body file. Please check the filename or format.")
        quit()
    
# Prepares email message to be sent with the appropriate fields
def constructMessage(fields,contact):
    message = EmailMessage()
    message['Subject'] = SUBJECT
    message['From'] = FROM
    message['To'] = contact['email']
    message.set_content(constructBody(fields,contact))
    return message

# Subroutine for sendEmails()
def sendEmail(fields,contact):
    try:
        SERVER.send_message(constructMessage(fields,contact))
        print(f"Email sent to {contact['email']}")
    except:
        print(f"Error while sending an email. Recipient's email is {contact['email']}. Please recheck the database.")
        quit()

# Uses a csv database to send emails with the fields from the csv file
def sendEmails():
    try:
        
        # Read database contents and send emails
        with open(DATABASE_FILENAME, 'r') as file:
            contacts = DictReader(file)
            fields = contacts.fieldnames
            for contact in contacts:
                sendEmail(fields, contact)
            file.close()
        
        # Deletes database content (just in case, nakakahiya kapag nagspam)
        with open(DATABASE_FILENAME, 'w') as file:
            file.close()

    except:
        print("Error with the database file. Please recheck filename.")
        quit()

initEmailService()
sendEmails()