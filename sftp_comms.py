from time import sleep
import pysftp # type: ignore

class SFTPClient:
    def __init__(self, host_port, host_username, host_password):
        self.host_port=host_port
        self.host_username=host_username
        self.host_password=host_password
        
    def getFileFromRobot(self, robot_file_dir, robot_file_path, local_download_path, SFTP_HOST, SFTP_USER, SFTP_PASS):
        with pysftp.Connection(host=SFTP_HOST, username=SFTP_USER, password=SFTP_PASS) as sftp:
            with sftp.cd(robot_file_dir):             # temporarily chdir to public
                    # upload file to public/ on remote
                sftp.get(robot_file_path, local_download_path)         # get a remote file
        sleep(5)
        print("SFTP connection closed after downloading.")
        
    # upload File
    def uploadToRobot(self, local_file_path, robot_file_dir, robot_file_name, SFTP_HOST, SFTP_USER, SFTP_PASS):
        with pysftp.Connection(host=SFTP_HOST, username=SFTP_USER, password=SFTP_PASS) as sftp:
            with sftp.cd(robot_file_dir):  # temporarily change directory to robot_file_dir
                sftp.put(local_file_path, robot_file_name)  # upload the file
        sleep(5)
        print("SFTP connection closed after uploading.")