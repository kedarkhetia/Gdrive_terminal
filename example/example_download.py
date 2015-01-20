from drive import drive

obj = drive.gdrive()
list_of_files = obj.retrieve_all_files()

#obj.print_all_files(list_of_files)


lst = []
count = 0
index = 0
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


obj.download(lst)
