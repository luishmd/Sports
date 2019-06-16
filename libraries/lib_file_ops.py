# Metadata
#=========
__author__ = "Luis Domingues"
__maintainer__ = "Luis Domingues"
__email__ = "luis.hmd@gmail.com"

# Description
#============
# Library used for general read/write operations


#----------------------------------------------------------------------------------------
# IMPORTS
#----------------------------------------------------------------------------------------
import os as os
import os.path as ospath


#----------------------------------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------------------------------
def is_file_empty(file, verbose=False):
    """
    Function that tests whether the file is empty. True if yes, otherwise False.
    """
    result = False
    try:
        if os.stat(file).st_size == 0:
            result = True
    except:
        if verbose:
            print("Invalid file <{}>".format(str(file)))
        else:
            pass
    return result


def get_files_complete_names_with_extensions(dir_path, file_extensions=[".*"], verbose=False):
    """
    Function that returns a list contaning the complete files names with extensions (e.g. ['C:/Users/luisd/Repos/sandbox_2/branches/gPB_Releases/gPB11/Library/gML/gML Auxiliary Correlations.gPJ-PB'] )
    """
    result = []
    try:
        # Directory exists
        files_names = os.listdir(dir_path)
        try:
            assert files_names
            # There are files
            for file in files_names:
                name, extension = ospath.splitext(file)
                if extension in file_extensions or ".*" in file_extensions:
                    file_complete_name = ospath.join(dir_path,file)
                    result.append(file_complete_name)
        except AssertionError:
            if verbose:
                print("Directory <{}> is empty".format(dir_path))
            else:
                pass
    except:
        if verbose:
            print("Could not find directory <{}>".format(dir_path))
        else:
            pass
    return result


def get_files_names_without_extensions(dir_path, file_extensions=[".*"], verbose=False):
    """
    Function that returns a list contaning the files names without extensions (e.g. ['gML Auxiliary Correlations'] )
    """
    result = []
    try:
        # Directory exists
        files_names = os.listdir(dir_path)
        try:
            assert files_names
            # There are files
            for file in files_names:
                name, extension = ospath.splitext(file)
                if extension in file_extensions or ".*" in file_extensions:
                    result.append(name)
        except AssertionError:
            if verbose:
                print("Directory <{}> is empty".format(dir_path))
            else:
                pass
    except:
        if verbose:
            print("Could not find directory <{}>".format(dir_path))
        else:
            pass
    return result


def get_files_pointers(dir_path, file_extensions=[".*"], verbose=False):
    """
    Function that returns the file pointer to each of the file with an extention in file_entensions
    """
    pointers_list = []
    files = get_files_complete_names_with_extensions(dir_path, file_extensions)
    for file in files:
        try:
            f = open(file,"r")
            pointers_list.append(f)
        except IOError:
            if verbose:
                print("Could not open file: <{}>".format(str(file)))
            else:
                pass
    return pointers_list


def write_to_file(file_object, what_to_write, verbose=False):
    """
    Function that writes what_to_write to a file
    """
    try:
        file_object.write(what_to_write)
        return file_object
    except:
        if verbose:
            print("Could not write to file <{}>.".format(file_object))
        else:
            pass
        return 1


def open_file(path, mode, verbose=False):
    """
    Function that opens a file and returns a file handle
    """
    try:
        f = open(path, mode)
        return f
    except:
        if verbose:
            print("Could not open file <{}>.".format(path))
        else:
            pass
        return 1

def close_file(file_handle, verbose=False):
    """
    Function that closes a file
    """
    try:
        file_handle.close()
        return 0
    except:
        if verbose:
            print ("Could not close file <{}>.".format(str(file_handle)))
        else:
            pass
        return 1

def delete_file(path, verbose=False):
        """
        Function that deletes a file
        """
        try:
            os.remove(path)
            return 0
        except:
            if verbose:
                print("Could not delete file <{}>.".format(path))
            else:
                pass
            return 1

#----------------------------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass

