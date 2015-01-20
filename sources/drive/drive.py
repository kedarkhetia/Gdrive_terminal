import os
import pprint
import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
from oauth2client.file import Storage
from apiclient import errors


class gdrive:
	
	def __init__(self):
		print 'GOOGLE-API-PYTHON-CLIENT'

		self.OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'
		self.CLIENT_SECRETS = 'client_secrets.json'

		storage = Storage('a_credentials_file')
		flow = oauth2client.client.flow_from_clientsecrets(self.CLIENT_SECRETS, self.OAUTH2_SCOPE)
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
		self.drive_service = apiclient.discovery.build('drive', 'v2', http=http)


	def upload(self,FILENAME,MIMETYPE,TITLE,DESCRIPTION):
		self.FILENAME = FILENAME
		self.MIMETYPE = MIMETYPE
		self.TITLE = TITLE
		self.DESCRIPTION = DESCRIPTION
		media_body = apiclient.http.MediaFileUpload(
		self.FILENAME,
		mimetype=self.MIMETYPE,
		resumable=True
		)

		body = {
		'title': self.TITLE,
		'description': self.DESCRIPTION,
		}

		new_file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
		pprint.pprint(new_file)
		
	def download(self):
		lst = []
		count = 0
		index = 0
		def retrieve_all_files(service):
		  result = []
		  page_token = None
		  while True:
		    try:
		      param = {}
		      if page_token:
			param['pageToken'] = page_token
		      files = service.files().list(**param).execute()

		      result.extend(files['items'])
		      page_token = files.get('nextPageToken')
		      if not page_token:
			break
		    except errors.HttpError, error:
		      print 'An error occurred: %s' % error
		      break
		  return result

		list_of_files = retrieve_all_files(self.drive_service)
		for line in list_of_files:
			print'\n'
			count = count + 1
			for subline in line:
				if subline == 'webContentLink':
					index = index + 1
					print 'INDEX: ',index
					lst.append(line[subline])
					print 'webContentLink: ',line[subline]
					print 'title: ',line['title'],'\n'


		download_index = int(raw_input('Enter downloadUrl index: '))
		download_url = lst[download_index-1]    

		dlink = 'wget '+ download_url
		abc = os.popen(dlink).read()	

