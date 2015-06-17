from drive import drive

obj = drive.gdrive()
list_of_files = obj.retrieve_all_files()
lst = obj.print_all_files(list_of_files)
#obj.download_if_flag()
