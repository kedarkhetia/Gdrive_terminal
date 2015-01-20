import os
from drive import drive

FILE = raw_input('path of file to upload : ')
cmd = 'zip backup.zip '+FILE+'/*' 
os.system(cmd)
FILENAME = 'backup.zip'

MIMETYPE = '*/*'
TITLE = raw_input('Title : ')
DESCRIPTION = raw_input('Discription : ')

obj = drive.gdrive()

obj.upload(FILENAME,MIMETYPE,TITLE,DESCRIPTION)


