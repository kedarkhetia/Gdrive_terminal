import os
from drive import drive

FILENAME = raw_input('path of file to upload : ')
#FILENAME = 'backup.zip'

MIMETYPE = '*/*'
TITLE = raw_input('Title : ')
DESCRIPTION = raw_input('Discription : ')

if(FILENAME.endswith('.txt')):
    MIMETYPE = 'text/plain'

obj = drive.gdrive()

obj.upload(FILENAME,MIMETYPE,TITLE,DESCRIPTION)
