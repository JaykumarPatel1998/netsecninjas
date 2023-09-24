
# Bell Geekfest 2023

## getting started
## Solution Sketch

### watcherscan - Automation tool to secure sensitive data on server

To ensure the protection of our resource target directory on the server, we have implemented the following solution:

1. We have created a file named `app.py` which serves as the main script for our solution. This script will continuously monitor the resource target directory on our server.

2. To achieve this continuous monitoring, we are utilizing the `watchdog` library from Python. This library allows us to track any changes or modifications made to the target directory.

3. As soon as we sense any modification event in the target directory, we notify the system admin on their email address about the malicious activity and trigger the encryption process.

4. The encryption process involves using a secure encryption algorithm to encrypt all the files and folders within the target directory. This ensures that the data remains confidential and cannot be easily compromised.

5. Before we initiate the encryption process, we commit the local target directory and push the latest commit hash -> unencrypted directory to a separate and secure location, The system admin is also notified via the email about backup commit hash. This location can be a remote server or a cloud storage service with strong security measures in place.

6. We also maintain watch logs of watchdog activity, where we store the *last modification date-time, process-id, file path, uid* on our server in *filemonitor.log,* this can also be exported to further inspect any activity on the server

7. In order to ensure data integrity, we have created a cron job that runs every few minutes and ensures that all the latest changes are committed to git <local> and these events are logged as commit hash in a separate log file *filemonitor.log*

## setting up watcherscan

### installing dependencies

```bash
  pip install requirements.txt
```

### setting up a cron job for continuous monitoring


```bash
 crontab -e
```

now paste the following cron job in the vim editor
```bash
 * * * * * username /path/to/script.sh
```

### Setting up your email for notification

update your <from_address> and <to_address> in app.py file

### run app.py file by passing a command line arguments
```python
 python3 app.py <target_path> <password_for_smtp_server>
```

update file trigger.sh to contain any trigger event you want
```bash
 #/bin/bash

# example - set up git on your target repo to access this feature
# cd <Path_to_target>
# git push -u origin main

echo "malicious event detected"

# implement file transfer process here
```







