import subprocess
import sys
import time
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64

# Set up logging
logging.basicConfig(filename='file_monitor.log', level=logging.INFO)


path_argument = None

def send_email(event, commitHash):
    fromaddr = "jaykumarpatel2710@gmail.com"
    toaddr = "slapbot6@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "System has been compromised : File change detected"
    body = f"Change detected: {event} \n latest git commit before system was compromised : {commitHash} "
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, path_argument)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Generate a key for encryption
password = 'password'.encode()  # This should be replaced by the actual password
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
cipher_suite = Fernet(key)

def get_latest_git_commit_hash(directory):
    # Change the working directory to the specified directory
    os.chdir(directory)

    # Get the latest git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

    # Return the commit hash
    return commit_hash.decode('utf-8')

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def process(self, event):
        print(get_latest_git_commit_hash('.'))
        logging.info(f'Event detected: {event}')
        send_email(event, get_latest_git_commit_hash('.'))
        for filename in os.listdir('target/'):  # This should be replaced by the actual directory
            path = os.path.join('target/' + filename)
            if os.path.isdir(filename):
                continue
            with open(path, 'rb') as file:
                encrypted_data = cipher_suite.encrypt(file.read())
            with open(path, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f'Encrypted file: {path}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py PASSWORD_for_smtp_server")
        sys.exit(1)

    # Get the path argument from the command line
    path_argument = sys.argv[1]
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='target/', recursive=True) 
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
