# add cmd code at the end of stance py to run the application code
# add class to sftp client comms
# follow flowchart

import os
from sftp_comms import SFTPClient
from stance import process_image
import numpy as np
import cv2  # type: ignore
from ultralytics import YOLO  # type: ignore
from time import sleep
import pysftp # type: ignore

# FTP Configuration for Pepper Robot
SFTP_HOST = '10.10.42.96' # Pepper's IP address
SFTP_PORT = 22 # Default SFTP port is 22 // FTP => port 21
SFTP_USER = 'nao'
SFTP_PASS = 'nao'

LOCAL_DOWNLOAD_PATH = "C:/Users/elias/OneDrive/Bureau/Karate_merge/html/pics/uploads"       
PROCESSED_OUTPUT_PATH = "C:/Users/elias/OneDrive/Bureau/Karate_merge/html/pics/output_image.jpg"

def main():
    data = ""
    # create SFTP Client to get the file from the remote location through SFTP
    SFTPClient1 = SFTPClient(SFTP_HOST, SFTP_USER, SFTP_PASS)
    with open(f"{LOCAL_DOWNLOAD_PATH}/tmp.txt", "w") as f:
        f.write("")
    SFTPClient1.getFileFromRobot(robot_file_path="tmp.txt",
                                        robot_file_dir='/home/nao/karate', 
                                        local_download_path=f"{LOCAL_DOWNLOAD_PATH}/tmp.txt",
                                        SFTP_HOST=SFTP_HOST,
                                        SFTP_USER=SFTP_USER,
                                        SFTP_PASS=SFTP_PASS)
    #open test
    with open(f"{LOCAL_DOWNLOAD_PATH}/tmp.txt","r") as f:
        data = f.read()
    if data == "start":
        SFTPClient1.getFileFromRobot(robot_file_path='stanceImage.jpg',
                                        robot_file_dir='/home/nao/karate', 
                                        local_download_path=LOCAL_DOWNLOAD_PATH,
                                        SFTP_HOST=SFTP_HOST,
                                        SFTP_USER=SFTP_USER,
                                        SFTP_PASS=SFTP_PASS)
        
        response = process_image(LOCAL_DOWNLOAD_PATH, PROCESSED_OUTPUT_PATH)
        with open(f"{LOCAL_DOWNLOAD_PATH}/response.txt","w") as f:
            if response:
                f.write("good")
            else:
                f.write("bad")
        SFTPClient1.uploadToRobot(SFTP_HOST=SFTP_HOST,
                                    SFTP_USER=SFTP_USER,
                                    SFTP_PASS=SFTP_PASS,
                                    robot_file_dir=f"/home/nao/karate/response.txt",
                                    robot_file_name="response.txt",
                                    local_file_path=f"{LOCAL_DOWNLOAD_PATH}/response.txt")
    
    sleep(10)
    os.system("python app.py")
    # os.kill()
    return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os.kill()