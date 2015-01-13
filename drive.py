import os
import pprint
import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
from oauth2client.file import Storage


print 'GOOGLE-API-PYTHON-CLIENT'

OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRETS = 'client_secrets.json'

storage = Storage('a_credentials_file')

FILE = raw_input('path of file to upload : ')
cmd = 'zip backup.zip '+FILE+'/*' 
os.system(cmd)
FILENAME = 'backup.zip'

MIMETYPE = '*/*'
TITLE = raw_input('Title : ')
DESCRIPTION = raw_input('Discription : ')

flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
 
print '\n'
credentials = storage.get()
print credentials

if credentials is None or credentials.invalid:
	authorize_url = flow.step1_get_authorize_url()
	print 'Go to the following link in your browser: ' + authorize_url
	code = raw_input('Enter verification code: ').strip()
	credentials = flow.step2_exchange(code)
	storage.put(credentials)
  
http = httplib2.Http()
credentials.authorize(http)
drive_service = apiclient.discovery.build('drive', 'v2', http=http)

media_body = apiclient.http.MediaFileUpload(
FILENAME,
mimetype=MIMETYPE,
resumable=True
)

body = {
'title': TITLE,
'description': DESCRIPTION,
}

new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(new_file)


