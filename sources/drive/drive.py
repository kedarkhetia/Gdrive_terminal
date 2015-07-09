import os
import pprint
import httplib2
import googleapiclient.discovery
import googleapiclient.http
import oauth2client.client
from oauth2client.file import Storage
from googleapiclient import errors
from googleapiclient.http import BatchHttpRequest


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
		self.drive_service = googleapiclient.discovery.build('drive', 'v2', http=http)

	def insert_permission(self, file_id , value, perm_type, role):
	  new_permission = {
	      'value' : value,
	      'type': perm_type,
	      'role': role
	  }
	  try:
	    return self.drive_service.permissions().insert(
		fileId=file_id, body=new_permission).execute()
	  except errors.HttpError, error:
	    print 'An error occurred: %s' % error
	  return None

	def upload(self,FILENAME,MIMETYPE,TITLE,DESCRIPTION):
		self.FILENAME = FILENAME
		self.MIMETYPE = MIMETYPE
		self.TITLE = TITLE
		self.DESCRIPTION = DESCRIPTION
		media_body = googleapiclient.http.MediaFileUpload(
		self.FILENAME,
		mimetype=self.MIMETYPE,
		resumable=True
		)

		body = {
		'title': self.TITLE,
		'description': self.DESCRIPTION
		}

		new_file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
		pprint.pprint(new_file)

	def upload(self,FILENAME,MIMETYPE,TITLE,DESCRIPTION,FOLDER_ID):
		self.FILENAME = FILENAME
		self.MIMETYPE = MIMETYPE
		self.TITLE = TITLE
		self.DESCRIPTION = DESCRIPTION
		media_body = googleapiclient.http.MediaFileUpload(
		self.FILENAME,
		mimetype=self.MIMETYPE,
		resumable=True
		)

			body = {
			'title': self.TITLE,
			'description': self.DESCRIPTION,
			 "parents": [{
			    "kind": "drive#parentReference",
			    "id": FOLDER_ID
			  	}]
			}

			new_file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
			pprint.pprint(new_file)

	def retrieve_all_files(self):
		  result = []
		  service = self.drive_service
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



	def print_all_files(self,list_of_files):
		self.lst = []
		self.lst_name = []
		self.flag_file = None
		self.count = 0
		self.index = 0
		self.list_of_files = list_of_files
		for line in list_of_files:
			print '\n'
			self.count = self.count + 1
			for subline in line:
				if subline == 'id':
					self.index = self.index + 1
					print 'INDEX: ',self.index
					try:
						self.lst.append(line['webContentLink'])
						print 'webContentLink: ',line['webContentLink']
					except:
						self.lst.append("NULL")
						print "This is a folder"

					self.lst_name.append(line['title'])
					print 'title: ',line['title']
					print 'ID : ',line['id']


	def get_folder_id(self,folder_name,list_of_files):
		for line in list_of_files:
			for subline in line:
				if line['title'] == folder_name:
					return line['id']


	def download(self,name):
		#self.lst = lst

		for i in range(len(self.lst_name)):
			if self.lst_name[i] == name:
				download_url = self.lst[i]
				stri = self.lst_name[i]

		dlink = 'wget '+ download_url
		abc = os.popen(dlink).read()

		lst1 = []
		lst2 = []
		string = download_url
		if(string.startswith("https://docs.google.com/")):
			lst1 = string.split('&')
			lst2 = lst1[0].split('/')

		os.popen('mv ' + lst2[3] + ' ' + stri)

	def download_if_flag(self):
			if(self.flag_file != None):
				dlink = 'wget ' + self.flag_file
				abc = os.popen(dlink).read()

				lst1 = []
				lst2 = []
				string = self.flag_file
				if(string.startswith("https://docs.google.com/")):
					lst1 = string.split('&')
					lst2 = lst1[0].split('/')

				os.popen('mv ' + lst2[3] + ' flag.txt')
