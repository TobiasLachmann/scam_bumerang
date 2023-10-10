import imaplib
import smtplib
import ssl
import email
import pandas as pd

nr = 0

credentials = pd.read_csv("accounts.csv")

print(credentials)
imap_server = credentials.loc[nr, "imap_server"]
email_adress = credentials.loc[nr, "email_adress"]
password = credentials.loc[nr, "password"]

# Login Read
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_adress, password)

# Login Send
context = ssl.create_default_context()
smtp_port = credentials.loc[nr, "smtp_port"]
smtp_server = credentials.loc[nr, "smtp_server"]

#TODO: Find Scam folder and use that
#imap.select("Inbox")
imap.select("Spamverdacht")

imap.search(None, "ALL")

_, msgnums = imap.search(None, "ALL")

emails_to_send_to = []

for msgnum in msgnums[0].split():
    _, data = imap.fetch(msgnum, "RFC822")
    message = email.message_from_bytes(data[0][1])
    print(f"Message Number: {msgnum}")
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('Subject')}")
    print(f"Reply-To: {message.get('Reply-To')}")
    # ('X-Report-Spam', 'complaints@episerver.com')
    # ('Return-Path', '<return@t.laurason-news.de>')
    # ('Message-ID', '<re-pLd1axQBFuy52h9d...n-news.de>'

    #Fitler

    # Add to send list
    emails_to_send_to.append({"receiver_mail": message.get('Reply-To')})
 


imap.close()


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(email_adress, password)

    for reply in emails_to_send_to:
        receiver_email = reply["receiver_mail"]


        send_message="""\
        Subject: Hi there

        This message is sent from Python."""



        server.sendmail(email_adress, receiver_email, send_message)
    server.quit()





print("End")




"""
Filterideen
- Newsletter
- noreply


"""

