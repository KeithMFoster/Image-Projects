import os
import glob
import smtplib
import mimetypes
import socket
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


def send_email(files_to_send):
    recipients = ['stoyercd@redrocketcorp.com', 'spencerka@redrocketcorp.com']
    emailfrom = 'channelserver@redrocketcorp.com'
    emailto = ', '.join(recipients)
    username = "channelserver@redrocketcorp.com"
    password = "Welcome1"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Image Processing Notification"

    body = MIMEText(files_to_send)
    msg.attach(body)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
    except socket.error:
        print 'Encountered an error sending email. Starting second attempt...'
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.sendmail(emailfrom, emailto, msg.as_string())
            server.quit()
        except socket.error:
            print 'Something went wrong. Try again.'
