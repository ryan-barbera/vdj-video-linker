import os
import glob
import sys


def get_all_file_paths_in_path(path_in):
    filePathArr = []
    exclude_directories = set(['\\~TEMP', '\\~VIDEOTANOSHII'])
    for dirpath, dirnames, filenames in os.walk(path_in):
        dirnames[:] = [d for d in dirnames if d not in exclude_directories]
        for file in filenames:
            filePathArr.append(dirpath + '\\' + file)
       
    return filePathArr
    

def get_latest_m3u(history_path) :

    if(any(glob.glob(history_path + '/*.m3u'))):
        list_of_files = glob.glob(history_path + '/*.m3u')
    elif(any(glob.glob(history_path + '/*.m3u8'))):
        list_of_files = glob.glob(history_path + '/*.m3u8')
    else:
        #File Path must be improperly defined, exit program
        sys.exit("Did not find history file in :"+ history_path +" exiting program...") 
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

#Reads latest .m3u file, 
def read_last_line(tracklist_path) :	
    with open(tracklist_path, "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        except IOError:
            print("Tracklist file not found, please check the path in the ini folder")
        last_line = file.readline().decode()
        #last_line = file.readline()
	#last_line = "In readend"
    file.close()
    return last_line
    
    
#Reads last two lines
def read_second_to_last_line(tracklist_path) :	
    num_newlines = 0
    with open(tracklist_path, "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while num_newlines < 2:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            file.seek(0)
        except IOError:
            print("Tracklist file not found, please check the path in the ini folder")
        last_line = file.readline().decode()
        #last_line = file.readline()
	#last_line = "In readend"
    file.close()
    return last_line
    
    
    
    
def see_if_file_exists_in_tmp( vidfolder_path):
    testpath = vidfolder_path + '\\~TEMP\\%(title)s.%(ext)s'
    if os.path.exists(testpath):
        return testpath
    else:
        return None
        
def see_if_file_exists(filePathIn):
    if os.path.exists(filePathIn):
        return True
    else:
        return False

def clean_temp_folder(vidfolder_path):
    path = vidfolder_path + '\\~TEMP'
    for filename in sorted(os.listdir(path))[:-10]:
        filename_relPath = os.path.join(path,filename)
        os.remove(filename_relPath)
    
    