import os
import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pyautogui

# recerive email
EMAIL = 'huytestmmt@gmail.com'
PASSWORD = 'duquochuy'
SERVER = 'imap.gmail.com'
# send email
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
FROM_ADDR = 'huytestmmt@gmail.com'
TO_ADDR = ['tcao135792@gmail.com']

MESSAGE = MIMEMultipart()
MESSAGE['From'] = FROM_ADDR
MESSAGE['To'] = ', '.join(TO_ADDR)


PATH_SCREENSHOT = 'Image/screenshot.jpg'



# login to receive 
# connect to the server and go to its inbox
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
# we choose the inbox but you can select others
mail.select('inbox')

# login to send 
server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(EMAIL, PASSWORD)

# screenshot
def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'Image\screenshot.jpg')
    print(1)

def sendImage(path):
    with open(path, 'rb') as f:
        img_data = f.read()

    MESSAGE['Subject'] = 'Reply Request Screenshot'

    #text = MIMEText("test")
    #message.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(path))
    MESSAGE.attach(image)
    print(2)



# we'll search using the ALL criteria to retrieve
# every message inside the inbox
# it will return with its status and a list of ids
status, data = mail.search(None, 'ALL')
# the list returned is a list of bytes separated
# by white spaces on this format: [b'1 2 3', b'4 5 6']
# so, to separate it first we create an empty list
mail_ids = []
# then we go through the list splitting its blocks
# of bytes and appending to the mail_ids list
for block in data:
    # the split function called without parameter
    # transforms the text or bytes into a list using
    # as separator the white spaces:
    # b'1 2 3'.split() => [b'1', b'2', b'3']
    mail_ids += block.split()

# now for every id we'll fetch the email
# to extract its content
for i in mail_ids:
    # the fetch function fetch the email given its id
    # and format that you want the message to be
    status, data = mail.fetch(i, '(RFC822)')

    # the content data at the '(RFC822)' format comes on
    # a list with a tuple with header, content, and the closing
    # byte b')'
    for response_part in data:
        # so if its a tuple...
        if isinstance(response_part, tuple):
            # we go for the content at its second element
            # skipping the header at the first and the closing
            # at the third
            msg = email.message_from_bytes(response_part[1])

            # with the content we can extract the info about
            # who sent the msg and its subject
            mail_from = msg['from']
            mail_subject = msg['subject']

            # then for the text we have a little more work to do
            # because it can be in plain text or multipart
            # if its not plain text we need to separate the msg
            # from its annexes to get the text
            if msg.is_multipart():
                mail_content = ''

                # on multipart we have the text msg and
                # another things like annex, and html version
                # of the msg, in that case we loop through
                # the email payload
                for part in msg.get_payload():
                    # if the content type is text/plain
                    # we extract it
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                # if the msg isn't multipart, just extract it
                mail_content = msg.get_payload()
            # and then let's show its result
            print(f'From: {mail_from}')
            print(f'Subject: {mail_subject}')
            print(f'Content: {mail_content}')
            print(mail_content.rstrip())
            if (mail_content.rstrip() == 'screenshot'):
                print(0)
                screenshot()
                sendImage(PATH_SCREENSHOT)


# infor to send email
# message = MIMEText('Hello World')
# message['subject'] = 'Hello'
# message['From'] = FROM_ADDR
# message['To'] = ', '.join(TO_ADDR)
# send mesage
server.sendmail(FROM_ADDR, TO_ADDR, MESSAGE.as_string())
server.quit()