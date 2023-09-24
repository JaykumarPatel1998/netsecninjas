# Bell Geekfest 2023 
# NetSecNinjas

## Solution Sketch

# Bell Geekfest 2023

## Solution Sketch

To ensure the protection of our resource target directory on the server, we have implemented the following solution:

1. We have created a file named `app.py` which serves as the main script for our solution. This script will continuously monitor the resource target directory on our server.
2. To achieve this continuous monitoring, we are utilizing the `watchdog` library from Python. This library allows us to track any changes or modifications made to the target directory.
3. As soon as we sense any modification event in the target directory, we trigger the encryption process. This ensures that the data within the directory is protected and cannot be accessed by unauthorized individuals.
4. The encryption process involves using a secure encryption algorithm to encrypt all the files and folders within the target directory. This ensures that the data remains confidential and cannot be easily compromised.
5. Before we initiate the encryption process , we push the latest commit hash  -> unencrypted directory to a separate and secure location. This location can be a remote server or a cloud storage service with strong security measures in place. we use github
