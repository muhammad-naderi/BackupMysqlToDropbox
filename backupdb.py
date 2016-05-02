#!/usr/bin/env /usr/local/bin/python3.5

import os
import time
import dropbox as dropbox
from time import sleep

user = "root" # Mysql user with appropriate privileges
password = "123" # Password for the Mysql user
database = "db_name" # Name of the database to backup
access_token = 'xxx' # The OAuth2.0 token from Dropbox Developers Page (https://www.dropbox.com/developers/apps)
folder = "/var/backup/script/" # This is the address in which you are going to save your script


def get_dump():
    file_stamp = time.strftime('%Y-%m-%d-%I:%M')
    
    os.popen("mysqldump -u %s -p%s -e --opt -c %s | bzip2 > %s.bz2" % (
        user, password, database, folder + database + "_" + file_stamp))

    print("Database dumped as " + database + "_" + file_stamp + ".bz2 --")

    return database + "_" + file_stamp + ".bz2"


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from=None, file_to=None):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f, file_to)


def send_to_dropbox(file_from):
    transfer_data = TransferData(access_token)

    file_from_abs = folder + file_from
    file_to = '/backup/' + file_from  # The full path to upload the file to, including the file name

    # API v2
    transfer_data.upload_file(file_from=file_from_abs, file_to=file_to)
    print("backup uploaded to dropbox")


def main():
    backup_name = get_dump()
    sleep(10)
    send_to_dropbox(backup_name)


if __name__ == '__main__':
    main()
