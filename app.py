import getpass
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
user = getpass.getuser()
logging.basicConfig(
    filename="watcher.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(process)d - %(message)s -" + f" {user}",
    datefmt="%Y-%m-%d %H:%M:%S",
)

password = None
target_path = None
from_address = "jaykumarpatel2710@gmail.com"
to_address = "slapbot6@gmail.com"

def send_email(event, commitHash):
    # Function to send email notification
    fromaddr = from_address
    toaddr = to_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "System has been compromised : File change detected"
    body = f"Change detected: {event} \n latest git commit before system was compromised : {commitHash} "
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
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
    # Function to get the latest Git commit hash
    # Change the working directory to the specified directory
    os.chdir(directory)

    # Get the latest git commit hash
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

    # Return the commit hash
    return commit_hash.decode('utf-8')

class MyHandler(FileSystemEventHandler):
    # Custom event handler class
    def on_modified(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def process(self, event):
        # Function to process file system events
        # Raising the flag and emailing sysAdmin
        print("⛔️ Malicious activity detected by watcher!")

        print("latest hash generated # "get_latest_git_commit_hash('.'))
        logging.info(f'Event detected: {event}')

        print("📧 Notifying system admin via email...")
        send_email(event, get_latest_git_commit_hash('.'))
        print("Email sent to " + to_address)

        print("🚀 Pushing unencrypted backup to the repo...")

        subprocess.run(['bash', 'trigger.sh'])
        # Encrypting all the data inside watcher directory.
        print("🧩 Encrypting all the data...")
        for filename in os.listdir(target_path):  # This should be replaced by the actual directory
            path = os.path.join(target_path + filename)
            if os.path.isdir(filename):
                continue
            with open(path, 'rb') as file:
                encrypted_data = cipher_suite.encrypt(file.read())
            with open(path, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f'Encrypted file: {path}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py target_path PASSWORD_for_smtp_server")
        sys.exit(1)

    # Get the path argument from the command line
    target_path = sys.argv[1]
    password = sys.argv[2]

    print("🔥 Monitoring for changes")
    print(f"🎯 Target set to :{target_path}")

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=target_path, recursive=True) 
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()