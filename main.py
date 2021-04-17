import os
import shutil

'''
I have a directory and a subdirectory called “annotations”. 
There are many files in directory, which are pngs. 
In the subdirectory, there are xml files. 
These xml files have the same basename as the pngs in the parent directory,
but just with a different filename extension (xml instead of png).
There are fewer xmls than pngs. Please write functions that output the following:
'''


class utils:
    def ignore_files(dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def make_backup_dir(directory):
    '''
    Copies the directory and its subdirectories and creates a
    sibling directory that is a duplicate with the same name with
    suffix "_backup" added at end.
    '''
    try:
        parent_directory = os.getcwd()
        old_dir = os.path.join(parent_directory, directory)
        backup_name = directory + "_backup"
        new_dir = os.path.join(parent_directory,backup_name)
        shutil.copytree(old_dir,new_dir)
    except FileExistsError:
        print(f"{backup_name} already exists!")
    return 

def make_excludes_dir(directory):
    '''
    Copies the directory and its subdirectories and creates a
    sibling directory that is a duplicate with the same name with
    suffix "_excludes" added at end. Return path to that directory.
    '''
    try:
        current = os.getcwd()
        parent_dir = os.path.join(current, directory)
        excludes_name =  directory + "_excludes"
        excludes_dir = os.path.join(current, excludes_name)
        shutil.copytree(parent_dir, excludes_dir, ignore=utils.ignore_files)
    except FileExistsError:
        print(f"{excludes_name} already exists!")
    return excludes_dir


def get_png_paths_for_annotations(directory):
    '''
    Given a subdirectory in directory called "annotations", which are xmls,
    return an array of all paths of all the corresponding pngs in directory
    which have the same file basenames but have a png extension.
    '''
    main_directory = os.getcwd()
    parent_dir = os.path.join(main_directory, directory)
    working_dir = os.path.join(parent_dir,"annotations")
    
    parent_files = os.listdir(parent_dir)
    annotation_files = os.listdir(working_dir)
    
    png_files = []

    for png_index, _png in enumerate(parent_files):
        for xml_index, _xml in enumerate(annotation_files):
                xml_file = _xml.split('.',3)[0]
                png_file = _png.split('.',3)[0]
                if xml_file == png_file:
                    png_files.append(_png)


    for i , _png in enumerate(png_files):
        png_files[i] = os.path.join(parent_dir, _png)
    
    return png_files

def get_png_paths_for_negative_annotations(png_paths, directory):
    '''
    Given a directory, return an array of all png files in that directory
    that are not in an array, called png_paths
    '''
    all_png_files = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            if f[-3:] == "png":
                all_png_files.append(os.path.abspath(os.path.join(dirpath, f)))
    
    paths_to_return = set(all_png_files) - set(png_paths)
    return paths_to_return

   
    
def move_to_excludes_directory(directory, excludes_dir, png_paths):
    '''
    Move each png, whose paths are provided in an array called png paths, from directory
    excludes_dir.
    '''
    for _file in png_paths:
        shutil.move(_file, excludes_dir)
    return

directory = "main"
make_backup_dir(directory)
excludes_dir = make_excludes_dir(directory)
get_png_paths_for_annotations(directory)
png_paths = get_png_paths_for_annotations(directory)
get_png_paths_for_negative_annotations(png_paths, directory)
move_to_excludes_directory(directory, excludes_dir, png_paths)
print("All done!")




