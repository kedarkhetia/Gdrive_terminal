import os
from drive import drive

FILENAME = raw_input('path of file to upload : ')
FOLDER_NAME = raw_input('folder to upload file in : ')
list_of_files = obj.retrieve_all_files()
FOLDER_ID = get_folder_id(FOLDER_NAME,list_of_files)

MIMETYPE = '*/*'
TITLE = raw_input('Title : ')
DESCRIPTION = raw_input('Discription : ')

if(FILENAME.endswith('.txt')):
    MIMETYPE = 'text/plain'

obj = drive.gdrive()

obj.upload(FILENAME,MIMETYPE,TITLE,DESCRIPTION,FOLDER_ID)
