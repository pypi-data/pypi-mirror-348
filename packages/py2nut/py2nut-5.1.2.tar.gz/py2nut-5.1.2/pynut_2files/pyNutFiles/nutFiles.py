try:
    from pynut_2files.pyNutFiles import _lib as lib
except:
    try:
        from pyNutFiles import _lib as lib
    except:
        try:
            from . import _lib as lib
        except:
            import _lib as lib
# Pynut
oth =       lib.nutOther()
dat =       lib.nutDate()
dframe =    lib.nutDataframe()
XlsFmt =    lib.nutXlsFormat()
XlsApp =    lib.nutXlsApp()
flCopy =    lib.nutCopy()
# Other
pd =        lib.pandas()
pickle =    lib.pickle()
shutil =    lib.shutil()
psutil =    lib.psutil()
glob =      lib.glob()
csv =       lib.csv()
ZipFile =   lib.ZipFile()
win32 =     lib.win32()
xw =        lib.xlwings()
xlsxwriter = lib.xlsxwriter()
xlrd =      lib.xlrd()
openpyxl =  lib.openpyxl()
pythoncom = lib.pythoncom()
logger =    lib.logger()
import os, sys
import time
import datetime as dt
import warnings
fDte_datePast = dat.fDte_datePast



# ------------------------------------------------------------------------------
# Files Characteristics
# ------------------------------------------------------------------------------
def fStr_myFileName(o_file=None):
    ''' Get the Python File Name '''
    if o_file is None:
        return os.path.basename(__file__)
    else:
        return os.path.basename(o_file)

def fStr_myPath(o_file=None):
    ''' Get the path of the Python File'''
    # os.getcwd()
    if o_file is None:
        return os.path.dirname(os.path.abspath(__file__))
    else:
        return os.path.dirname(os.path.abspath(o_file))

def fStr_GetEnvUserName():
    ''' Get the Environment of the USERPROFILE'''
    return os.environ['USERPROFILE']

def fStr_GetUserEmail(str_emailExtension='@gmail.com'):
    ''' Get the Corporate Email of the user '''
    str_env = fStr_GetEnvUserName()
    str_env = str_env.replace(r'C:\Users' + '\\', '')
    return str_env + str_emailExtension

def fStr_GetFolderFromPath(str_path):
    ''' Get the Folder from a file path '''
    str_folder = str('\\'.join(str_path.split('\\')[:-1]))
    return str_folder

def fStr_GetFileFromPath(str_path):
    ''' Get the file Name from a file path '''
    str_fileName = str(str_path.split('\\')[-1])
    return str_fileName

def fStr_BuildPath(str_folder, str_FileName):
    if str_FileName == '':
        str_path = str_folder
    elif str_folder == '':
        str_path = str_FileName
    else:
        str_path = os.path.join(str_folder, str_FileName)
    return str_path

def fStr_BuildFolder_wRoot(str_folderPart, str_folderRoot):
    if str_folderPart[:2] == '\\\\':
        return str_folderPart
    elif str_folderPart[:2] == 'C:':
        return str_folderPart
    elif str_folderPart[:2] == 'E:':
        return str_folderPart
    elif 'Manual_py' in str_folderPart:
        str_newRoot = str_folderRoot.replace('Auto_py\\', '')
        return os.path.join(str_newRoot, str_folderPart)
    else:
        return os.path.join(str_folderRoot, str_folderPart)

def fL_getEnvironmentPythonPaths():
    l_paths = os.environ['PATH'].split(os.pathsep)
    return l_paths


# ------------------------------------------------------------------------------
# List Files in folder
# ------------------------------------------------------------------------------
def fL_listFile(str_path):
    """ Listing all files and folder in a folder using the library glob """
    l_fileList = glob.glob(os.path.join(str_path, '*'))
    return l_fileList

def fList_FileInDir(str_path):
    """ Listing all files and folder in a folder using the library os """
    try:
        l_fic = os.listdir(str_path)
    except Exception as err:
        logger.error('  ERROR in fList_FileInDir |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        raise
    return l_fic

def fList_FileInDir_Txt(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.txt' in fic]
    except Exception as err:
        logger.error('  ERROR in fList_FileInDir_Txt |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        raise
    return l_fic

def fList_FileInDir_Csv(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.csv' in fic]
    except Exception as err:
        logger.error('  ERROR in fList_FileInDir_Csv |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        raise
    return l_fic

def fList_FileInDir_Py(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.py' in fic]
    except Exception as err:
        logger.error('  ERROR in fList_FileInDir_Py |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        raise
    return l_fic

def fBl_FileExist(str_path):
    """ Test if a file exist. Giving a path, return a Boolean """
    if os.path.isfile(str_path):
        return True
    else:
        return False

def fBl_FolderExist(str_path):
    """ Test if a folder exist. Giving a folder path, return a Boolean """
    if os.path.exists(str_path):
        return True
    else:
        return False

@oth.dec_stopProcessTimeOut(int_secondesLimit=10, returnIfTimeOut=False)
def fBl_FolderExist_timeout(str_path):
    """ Test if a folder exist. Giving a folder path, return a Boolean
    The function is decorated not to search for more than 10 secondes """
    return fBl_FolderExist(str_path)

def UpdateTxtFile(str_path, str_old, str_new=''):
    with open(str_path, 'r') as file:
        str_text = file.read()
    # Replace the target string
    str_text = str_text.replace(str_old, str_new)
    # Write the file out again
    with open(str_path, 'w') as file:
        file.write(str_text)


# ------------------------------------------------------------------------------
# Trim Files
# ------------------------------------------------------------------------------
def TrimTxtFile(str_path, bl_right=False, bl_left=False):
    """ LEGACY Function
    By Default the Separator is = \t"""
    TrimTxtFile_comma(str_path, bl_right=bl_right, bl_left=bl_left, str_sep='\t')

def TrimTxtFile_comma(str_path, bl_right=False, bl_left=False, str_sep=','):
    """ This function will Trim the space in a text file
    We can decide to Trim only the space on the left or right
    By default, the Trim is both side"""
    with open(str_path, 'r') as file:
        # l_lines = file.readlines()
        l_lines = file.read().splitlines()
    if bl_right is True:
        if str_sep == '\t':
            l_lines_2 = [line.rstrip() + '\n' for line in l_lines]
        else:
            l_lines_2 = [line.rstrip(str_sep) + '\n' for line in l_lines]
    elif bl_left is True:
        if str_sep == '\t':
            l_lines_2 = [line.lstrip() + '\n' for line in l_lines]
        else:
            l_lines_2 = [line.lstrip(str_sep) + '\n' for line in l_lines]
    else:
        if str_sep == '\t':
            l_lines_2 = [line.strip() + '\n' for line in l_lines]
        else:
            l_lines_2 = [line.strip(str_sep) + '\n' for line in l_lines]
    # Write the file out again
    with open(str_path, 'w') as file:
        file.writelines(l_lines_2)

def TrimCsvFile(str_path, bl_right=False, bl_left=False):
    """ This function will Trim the space in a CSV file
    We can decide to Trim only the space on the left or right
    By default, the Trim is both side"""
    with open(str_path, 'r') as file:
        o_reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
        ll_content = [[x for x in row] for row in o_reader]
        # prrint('ll_content', ll_content)
        ll_content2 = []
        # Choose the L or R Trim
        if bl_right is True:
            i_sens = -1
        elif bl_left is True:
            i_sens = 1
        else:
            i_sens = False
        # remove spaces
        if i_sens is False:
            ll_content2 = [[elmt for elmt in l_line if elmt != ''] for l_line in ll_content]
        else:
            for l_line in ll_content:
                for elmt in l_line[::i_sens]:
                    if elmt != '':      break
                    if l_line == []:    break
                    l_line = l_line[:-1]
                ll_content2.append(l_line)
        # Remove the emtpy list at the end
        for l_line in ll_content2[::-1]:
            if l_line != []:            break
            ll_content2 = ll_content2[:-1]
        # prrint('ll_content2', ll_content2)
    # Write the file out again
    with open(str_path, 'w', newline='') as file:
        wtr = csv.writer(file)
        # for l_line in ll_content2:
        wtr.writerows(ll_content2)

def TrimTxtFichier_EOF(str_path, str_sep=','):
    """ This function will Trim the space in a TXT file
    Only at the end of the file: the empty rows """
    with open(str_path, 'r') as file:
        # l_lines = file.readlines()
        l_lines = file.read().splitlines()
    # remove spaces
    int_remove = 0
    for _line in l_lines[::-1]:
        _line_noSep = _line
        # TODO: test if that works with ','
        _line_noSep = _line_noSep.strip()
        # _line_noSep = _line_noSep.strip(str_sep)
        if not _line_noSep == '':
            break
        else:
            int_remove += 1
    # Remove End rows
    if not int_remove == 0:
        l_lines = [line + '\n' for line in l_lines[:-int_remove]]
        # Write the file only if sth has changed
        with open(str_path, 'w') as file:
            file.writelines(l_lines)

def TrimCsvFichier_EOF(str_path):
    """ This function will Trim the space in a CSV file
    Only at the end of the file: the empty rows """
    with open(str_path, 'r') as file:
        o_reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
        ll_content = [[x for x in row] for row in o_reader]
        # Remove the emtpy list at the end
        int_nbColFile = len(ll_content[0])
        ll_content = fLl_removeEmptyRows_EOF(ll_content, int_nbColFile)
    # Write the file out again
    with open(str_path, 'w', newline='') as file:
        wtr = csv.writer(file)
        # for l_line in ll_content2:
        wtr.writerows(ll_content)

def fLl_removeEmptyRows_EOF(ll_content, int_nbColFile=None):
    ''' Remove the emtpy list at the end'''
    if int_nbColFile is None:
        for l_line in ll_content[::-1]:
            if l_line != []:
                break
            ll_content = ll_content[:-1]
    else:
        for l_line in ll_content[::-1]:
            if l_line != [''] * int_nbColFile:
                break
            ll_content = ll_content[:-1]
    return ll_content


# ------------------------------------------------------------------------------
# Open Files
# ------------------------------------------------------------------------------
def fBk_OpenWk_xlrd(str_path):
    try:
        o_Book = xlrd.open_workbook(str_path)
    except Exception as err:
        logger.error(f' ERROR in fBk_OpenWk_xlrd (fl): |{err}| ')
        raise
    return o_Book

def fL_getSheetName_xls(str_path):
    try:
        l_sheetName = pd.ExcelFile(str_path).sheet_names
        # # LEGACY VERSION
        # l_wkSheet = pd.read_excel(str_pathModel, None).keys()
        # # OR
        # o_Book = fBk_OpenWk_xlrd(str_path)
        # l_sheetName = o_Book.sheet_names()
    except Exception as err:
        logger.error(f' ERROR in fL_getShtNam_xls (fl): |{err}| ')
        raise
    return l_sheetName


# ------------------------------------------------------------------------------
# Transform Names
# ------------------------------------------------------------------------------
def Act_Rename(str_folder, str_OriginalName, str_NewName, bl_message=True):
    """ Renaming a file and if it failed using the lib os, it will MOVE the file with shutil """
    try:
        if str_NewName.upper() != str_OriginalName.upper():
            if bl_message:
                logger.warning(' RENAMING from |{}|   to   |{}|'.format(str_OriginalName, str_NewName))
            try:
                os.rename(fStr_BuildPath(str_folder, str_OriginalName),
                          fStr_BuildPath(str_folder, str_NewName))
            except:
                shutil.move(fStr_BuildPath(str_folder, str_OriginalName),
                            fStr_BuildPath(str_folder, str_NewName))
    except Exception as err:
        logger.error('  ERROR in Act_Rename |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|-|{}|'.format(str_OriginalName, str_NewName))
        raise
    return True

def fStr_TransformFilName_fromXXX_forGlobFunction(str_fileName_withX, bl_exactNumberX=False):
    """ Change a string with unknown characters (XXXX) into sth understandable by the glob library
    'file_{*}_1.zip' ==> 'file_*_1.zip'     ( bl_exactNumberX = False)
    'file_{XXXX}_1.zip' ==> 'file_????.zip' ( bl_exactNumberX = True)
    'file_{XXXX}.zip' ==> 'file_*.zip'      ( bl_exactNumberX = False)
    """
    # Check if its a single {*}
    if '{*}' in str_fileName_withX:
        str_fileName_withX = str_fileName_withX.replace('{*}', '{X}')

    # Check if its a normal Name without {X}:
    if '{X' not in str_fileName_withX and 'X}' not in str_fileName_withX:
        return str_fileName_withX

    # Count the Number of Series of {XX}
    int_nbXX = str_fileName_withX.count('{X')
    int_nbXX2 = str_fileName_withX.count('X}')
    if int_nbXX != int_nbXX2:
        logger.error('   ERROR, check the sting str_fileName_withX in fStr_TransformFilName_fromXXX:  |{}|'.format(
            str_fileName_withX))
        return str_fileName_withX

    # Count the number of X in each Series of {XX}
    str_fileName = str_fileName_withX
    nb = 1
    while nb in range(1, int_nbXX + 1):
        nb += 1
        str_XXX = ''
        for i in range(1, 100):
            str_XXX = '{' + i * 'X' + '}'
            if str_fileName.count(str_XXX) > 0:
                nb = nb + str_fileName.count(
                    str_XXX) - 1  # just in case there is several time the same XXX, we dont want to pass again on this loop
                break
                # ==================================================
        # Exact Number ???????????????????????????????
        if bl_exactNumberX:
            int_lenXX = len(str_XXX) - 2
            str_fileName = str_fileName.replace(str_XXX, int_lenXX * '?')
        # Flex Number ?
        else:
            str_fileName = str_fileName.replace(str_XXX, '*')
        # ==================================================
    return str_fileName

# Return a list of File in a folder
def fL_GetFileListInFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible=False, bl_exactNumberX=True):
    """ Return the list of files in a folder that match the pattern given of the fileName
    with {*} or {XXX} within """
    if str_folder[-1] != '\\': str_folder += '\\'

    try:
        # Transform fiel name to be understood from 'glob.glob'
        str_fileName = fStr_TransformFilName_fromXXX_forGlobFunction(str_fileName_withX, bl_exactNumberX)
        # if no change, just return default
        if str_fileName == str_fileName_withX:
            return [str_folder + str_fileName_withX]

        # Using Glob function
        for file in [glob.glob(str_folder + str_fileName)]:
            if len(file) > 0:
                L_files = glob.glob(str_folder + str_fileName)
                # L_files = fL_listFile(os.path.join(str_folder, str_fileName))
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++
                return L_files
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Do not raise an issue if its a search, just return File with XX
            elif bl_searchOnlyIfPossible is True:
                # prrint(' Return the file with the X (Search only): ', str_fileName_withX)
                return [str_folder + str_fileName_withX]
            else:
                if bl_exactNumberX:
                    logger.warning(
                        ' EMPTY fL_GetFileListInFolder with exact number of X... We will now search with more flex')
                    l_filesFlex = fL_GetFileListInFolder(str_folder, str_fileName_withX, False, False)
                    return l_filesFlex
                else:
                    logger.warning('  EMPTY: file not found in fL_GetFileListInFolder')
                    raise
    except Exception as err:
        logger.error('  ERROR in fL_GetFileListInFolder |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|'.format(str_fileName_withX))
        raise
    return False

def fStr_GetMostRecentFile_InFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible=False,
                                    bl_exactNumberX=True):
    """ Return the list of files in a folder that match the pattern given of the fileName
    with {*} or {XXX} within
    AND take the most recent one"""
    if str_folder[-1] != '\\': str_folder += '\\'
    # Get the lisyt of matching files
    try:
        str_fileName_withX = str_fileName_withX.replace('{*}', '{X}')
        L_FileInFolder = fL_GetFileListInFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible,
                                                bl_exactNumberX)
    except Exception as err:
        logger.error('  ERROR fStr_GetMostRecentFile_InFolder |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|'.format(str_fileName_withX))
        raise
    # Return the most recent file
    try:
        if L_FileInFolder == []:    logger.error('  ERROR fStr_GetMostRecentFile_InFolder, L_FileInFolder is empty')
        # str_latest_file = max(L_FileInFolder, key = os.path.getmtime)       # Time of Update
        str_latest_file = max(L_FileInFolder, key=os.path.getctime)  # Time of Creation
        str_fileName = str_latest_file.replace(str_folder, '')
    except Exception as err:
        if bl_searchOnlyIfPossible: return str_fileName_withX
        logger.error('  ERROR fStr_GetMostRecentFile_InFolder 2 |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|'.format(str_fileName_withX))
        raise
    return str_fileName

def fL_GetFileList_withinModel(L_FileName, str_fileName_withX):
    """ If you have in memory a list of File Name
    you want to return the list of those who match the pattern given of the fileName
    with {*} or {XXX} within
    """
    try:
        # Check if its a normal Name without {X}:
        if '{X' not in str_fileName_withX and 'X}' not in str_fileName_withX and '{*}' not in str_fileName_withX:
            L_FileName = [fil for fil in L_FileName if str_fileName_withX.lower() in fil.lower()]
            return L_FileName
        # Count the Number of Series of {XX}
        int_nbXX = str_fileName_withX.count('{X')
        int_nbXX2 = str_fileName_withX.count('X}')
        if int_nbXX != int_nbXX2:
            logger.error('   ERROR, check the string str_fileName_withX in fL_GetFileList_withinModel: |{}|'.format(
                str_fileName_withX))
            return L_FileName
        # Count the number of X in each Series of {XX}
        str_fileName = str_fileName_withX
        for nb in range(1, int_nbXX + 1):
            str_XXX = ''
            for i in range(1, 15):
                str_XXX = '{' + i * 'X' + '}'
                if str_fileName.count(str_XXX) == 1: break
            str_fileName = str_fileName.replace(str_XXX, '{*}')
        # END
        l_fileName_part = str_fileName.split('{*}')
        l_files = L_FileName
        for name_part in l_fileName_part:
            l_files = [fil for fil in l_files if name_part.lower() in fil.lower()]
    except Exception as err:
        logger.error('  ERROR in fL_GetFileList_withinModel |{}|'.format(err))
        logger.error('  - ** ARGS : |{}|-|{}|'.format(str_fileName_withX, '|'.join(L_FileName)))
        raise
    return l_files


# ------------------------------------------------------------------------------
# Files Date
# ------------------------------------------------------------------------------
def fDte_GetModificationDate(str_pathFile):
    """ Function Get the Modification Date of a file
    Useful for Update of App
    """
    try:
        if fBl_FileExist(str_pathFile):
            dte_modif = os.path.getmtime(str_pathFile)
            # dte_modif = dat.fDte_formatToTimeStamp(dte_modif)
            dte_modif = dt.datetime.fromtimestamp(dte_modif)
        else:
            logger.warning('  fDte_GetModificationDate: File does not exist: ')
            logger.warning('  - Path : |{}|'.format(str_pathFile))
            return False
    except Exception as err:
        logger.error('  ERROR in fDte_GetModificationDate |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_pathFile))
        raise
    return dte_modif

def fL_KeepFiles_wTimeLimit(l_pathFile, dte_after=10, dte_before=0):
    """ Filter a list of file Path to return the files that has been updated
    after X days in the past and before Y days in the past
    dte_after and dte_before can be date or integer of days in the past
    """
    # Parameters in
    if type(dte_after) == int:
        dte_after = fDte_datePast(dte_after)
    if type(dte_before) == int:
        if dte_before != 0:
            dte_before = fDte_datePast(dte_before)
    # Keep file in list within the Limit Date
    try:
        l_pathReturn = [path for path in l_pathFile if fBl_FileExist(path)]
        l_pathReturn = [path for path in l_pathReturn if fDte_GetModificationDate(path) > dte_after]
        if dte_before != 0:
            l_pathReturn = [path for path in l_pathReturn if fDte_GetModificationDate(path) <= dte_before]
    except Exception as err:
        logger.error(' ERROR in fL_KeepFiles_wTimeLimit: |{}|'.format(err))
        raise
    return l_pathReturn

def fBl_fileTooOld(str_path, int_dayHisto=5):
    """ Return a boolean to know if a file is older than N days in the past """
    try:
        dte_delete = fDte_datePast(int_dayHisto)
        dte_ModificationDate = fDte_GetModificationDate(str_path)
        # File not exisiting
        if dte_ModificationDate is False:
            return False
        elif dte_ModificationDate < dte_delete:
            return True
        else:
            return False
    except Exception as err:
        logger.error('  ERROR in fBl_fileTooOld |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - ** ARGS : |{}|'.format(int_dayHisto))
        raise
    return False

def del_fichier_ifOldEnought(str_folder, str_fileName, int_dayHisto=5):
    """ Check is a file is older than N days in the past
    And if so, delete it
    If the folder where the file is supposed to be does not exist, the function will create it"""
    # Build Path
    if str_fileName == '':
        str_path = str_folder
        str_folder = '\\'.join(str_folder.split('\\')[:-1])
    else:
        str_path = fStr_BuildPath(str_folder, str_fileName)
    # if folder does not exist : sortir de la fonction sans delete rien (et en ayant creer le dossier)
    if fBl_createDir(str_folder):
        logger.warning(' Information: Folder was not existing (in del_fichier_ifOldEnought):  |{}|'.format(str_folder))
        return False
    # Boolean
    bl_tooOld = fBl_fileTooOld(str_path, int_dayHisto)
    # DELETE or not
    if bl_tooOld:
        os.remove(str_path)
    return 0


# -----------------------------------------------------------------
# CREATE
# -----------------------------------------------------------------
def fBl_createDir(str_folder):
    """ Create a Directory
    Return False if Directory exists, True if the folder has been created """
    try:
        if os.path.exists(str_folder):
            return False  # Folder already exist
        else:
            os.makedirs(str_folder)
    except Exception as err:
        logger.error('  ERROR: fBl_createDir - Program could NOT create the Directory: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        raise
    return True

def act_createFile(bl_folderRelative, str_folder, str_fileName='test.txt', str_text=''):
    dir_current = os.getcwd()
    try:
        # Define folder
        if bl_folderRelative:
            str_folder = os.getcwd().replace(str_folder, '') + str_folder
        # Create folder
        fBl_createDir(str_folder)
        # Change Dir
        os.chdir(str_folder)
    except Exception as err:
        logger.error('  ERROR in act_createFile |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|'.format(str_fileName))
        raise
    # Create File
    try:
        f = open(str_fileName, "w+")
    except Exception as err:
        try:
            os.chdir(dir_current)
        except Exception as err2:
            logger.error(
                '  ERROR: act_createFile - os.chdir(dir_current) did not work -- f = open(str_fileName,  |{}|'.format(
                    err2))
        logger.error(' ERROR: act_createFile - Could not create the file |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - ** ARGS : |{}|'.format(str_fileName))
        raise
    try:
        f.write(str_text)
        f.close()
    except Exception as err:
        # ------------------------
        try:
            f.close()
        except Exception as err2:
            logger.error(' ERROR: act_createFile - f.close():  |{}|'.format(err2))
        try:
            os.chdir(dir_current)
        except Exception as err3:
            logger.error(' ERROR: act_createFile - os.chdir() did not work -- f.write(str_text):  |{}|'.format(err3))
        # ------------------------
        logger.error('  ERROR: act_createFile - Could not write in the file: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_fileName))
        logger.error('  - Txt : |{}|'.format(str_text))
        raise
    try:
        os.chdir(dir_current)
    except Exception as err:
        logger.error('  ERROR: act_createFile - os.chdir(dir_current) did not work |{}|'.format(err))
        raise
    return 0

def fStr_CreateTxtFile(str_folder, str_FileName, df_data, str_sep='', bl_header=False, bl_index=False,
                       o_quoting=csv.QUOTE_MINIMAL, o_quotechar='"', o_escapechar=None):
    try:
        if str_FileName == '':      str_path = str_folder
        else:                       str_path = fStr_BuildPath(str_folder, str_FileName)
        if str_sep == '':           str_sep = ','
        elif str_sep == '\\t':      str_sep = '\t'
        # Create Folder if needed
        fBl_createDir(fStr_GetFolderFromPath(str_path))
        # TO CSV
        df_data.to_csv(str_path, sep=str_sep,
                       header=bl_header, index=bl_index,
                       quoting=o_quoting, quotechar=o_quotechar, escapechar=o_escapechar
                       )
        # csv.QUOTE_MINIMAL =       0
        # csv.QUOTE_ALL =           1
        # csv.QUOTE_NONNUMERIC =    2
        # csv.QUOTE_NONE =          3
    except Exception as err:
        logger.error('  ERROR in fl fStr_CreatTxtFile: Could not create the file: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - ** ARGS : |{}|-|{}|-|{}|-|{}|'.format(str_sep, bl_header, bl_index, o_quoting))
        raise
    return str_path


# -----------------------------------------------------------------
# READ
# -----------------------------------------------------------------
def fDf_readCsv(str_path, bl_header=None):
    """ Here only for more accessibility
    Use pd.read_csv with more flexibility"""
    # df_data = pd.read_csv(str_path, header = bl_header)
    df_data = dframe.fDf_readCsv_enhanced(str_path, bl_header=bl_header)
    return df_data

def fDf_readTxt(str_path, bl_header=None):
    """ Here only for more accessibility"""
    df_data = fDf_readCsv(str_path, bl_header=bl_header)
    return df_data

def fO_readfile_parquet(str_path, **d_options):
    """ fO_readfile_parquet reads parquet - require the libraries : pyarrow / fastparquet
    options: use_threads, engine='fastparquet', ... """
    o_file = pd.read_parquet(str_path, **d_options)
    return o_file

def fStr_ReadFile_sql(str_filePath):
    """ fStr_ReadFile_sql Opens and read the file as a single buffer"""
    file = open(str_filePath, 'r')
    str_Content = file.read()
    file.close()
    return str_Content

def fStr_readFile(bl_folderRelative, str_folder, str_fileName='test.txt'):
    dir_current = os.getcwd()
    try:
        # Define folder
        if bl_folderRelative:
            str_folder = os.getcwd().replace(str_folder, '') + str_folder
        # Check folder exist
        if not os.path.exists(str_folder):
            logger.error('  ERROR: fStr_readFile - Folder does not exist')
            logger.error('  - Path : |{}|'.format(str_folder))
            logger.error('  - fileName : |{}|'.format(str_fileName))
            raise
        # Change Dir
        os.chdir(str_folder)
    except Exception as err:
        logger.error('  ERROR in fStr_readFile |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_fileName))
        logger.error('  - ** ARGS : |{}|'.format(bl_folderRelative))
        raise
    # Read File
    try:
        f = open(str_fileName, "r")
    except Exception as err:
        # -------------------------------------
        try:
            os.chdir(dir_current)
        except Exception as err2:
            logger.error(
                '  ERROR: fStr_readFile - os.chdir(dir_current) did not work -- f = open(str_fileName: |{}|'.format(
                    err2))
        # -------------------------------------
        logger.error('  ERROR in fStr_readFile - Could not Open the file |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_fileName))
        logger.error('  - ** ARGS : |{}|'.format(bl_folderRelative))
        raise
    try:
        str_return = f.read()
        f.close()
    except Exception as err:
        # -------------------------------------
        try:
            f.close()
        except Exception as err2:
            logger.error('  ERROR in fStr_readFile - f.close |{}|'.format(err2))
        try:
            os.chdir(dir_current)
        except Exception as err3:
            logger.error('  ERROR: fStr_readFile - os.chdir(dir_current) did not work |{}|'.format(err3))
        # -------------------------------------
        logger.error('  ERROR: fStr_readFile- Could not Read the file |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_fileName))
        logger.error('  - ** ARGS : |{}|'.format(bl_folderRelative))
        raise
    try:
        os.chdir(dir_current)
    except Exception as err:
        logger.error(' ERROR: fStr_readFile - os.chdir(dir_current) did not work |{}|'.format(err))
        raise
    return str_return


# ------------------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------------------
def del_fichier(str_folder, str_fileName='', bl_ignoreErr=False):
    """ Delete a file """
    try:
        if str_fileName == '':
            str_path = str_folder
        else:
            str_path = fStr_BuildPath(str_folder, str_fileName)
        os.remove(str_path)
    except Exception as err:
        logger.error('  ERROR in del_ficher |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_fileName))
        if bl_ignoreErr is False:   raise
    return True


# -----------------------------------------------------------------
# ZIP
#   https://docs.python.org/3/library/zipfile.html
# -----------------------------------------------------------------
def ZipExtractFile(str_ZipPath, str_pathDest='', str_FileName='', bl_extractAll=False, str_zipPassword=''):
    try:
        # If the Zip has a password, better to extract all at once
        if str_zipPassword != '':
            bl_extractAll = True
        # Open the ZIP
        with ZipFile(str_ZipPath, 'r') as zipObj:
            if str_zipPassword != '':
                zipObj.setpassword(pwd=bytes(str_zipPassword, 'utf-8'))
            if bl_extractAll:
                # Extract all the file
                if str_pathDest == '':
                    zipObj.extractall()
                else:
                    zipObj.extractall(str_pathDest)
                time.sleep(5)
            else:
                # Get a list of all archived file names from the zip
                l_fileInZip = zipObj.namelist()
                # Get The name of the list  matching
                l_fileInZip_file = fL_GetFileList_withinModel(l_fileInZip, str_FileName)
                # Extract the file
                for file in l_fileInZip_file:
                    zipObj.extract(file, str_pathDest)
    except Exception as err:
        logger.error(' ERROR: ZipExtractFile || {}'.format(str(err)))
        if bl_extractAll:
            logger.error('  - ** ARGS : |{}|-|{}|-|{}|'.format(str_ZipPath, str_pathDest, str_zipPassword))
            raise
        else:
            logger.error('  - Failed to download the file : |{}|'.format(str_FileName))
            try:
                logger.error('  - File List in the Zip : |{}|'.format('|'.join(l_fileInZip)))
            except:
                logger.error(' - No  l_fileInZip defined')
            logger.error(' (**) Trying to extract all files...')
            ZipExtractFile(str_ZipPath, str_pathDest, '', True, str_zipPassword)
    return True

def ZipCompressFiles(str_ZipPath, l_pathDest):
    try:
        with ZipFile(str_ZipPath, 'w') as zipObj:
            for _file in l_pathDest:
                zipObj.write(_file, arcname=fStr_GetFileFromPath(_file))
                # , compress_type = zipfile.ZIP_DEFLATED
    except Exception as err:
        logger.error(' ERROR: ZipCompressFiles |{}| '.format(str(err)))
        logger.error('  - str_ZipPath : |{}|'.format(str_ZipPath))
        logger.error(l_pathDest)
        raise
    return True


# -----------------------------------------------------------------
# PICKLE - Compressed file
# -----------------------------------------------------------------
def pickle_load(str_path):
    if not os.path.isfile(str_path):
        return None
    # for reading also binary mode is important
    with open(str_path, 'rb') as dbfile:
        db = pickle.load(dbfile)
    return db


def pickle_store(str_path, o_data, bl_replace=False):
    try:
        if bl_replace is True:
            with open(str_path, 'wb') as dbfile:
                pickle.dump(o_data, dbfile)
        else:
            with open(str_path, 'ab') as dbfile:
                pickle.dump(o_data, dbfile)
        return True
    except Exception as err:
        logger.error(f'ERROR in pickle_store: |{err}|')
        raise


# -----------------------------------------------------------------
# READ XLS / XLSX Files
# -----------------------------------------------------------------
def pd_read_excel(str_path, str_SheetName='', bl_header=None):
    """ To be able to read xlsx files with the function: |pd.read_excel|
        You need to have a previous xlrd version (xlrd==1.2.0)
        And replace the file xlsx.py (/Lib/site-packages/xlrd) by the one in this library !!!
        If it fails the engine openxyl will be used
        You can pass a sheet_name and a header as input
        """
    try:
        if str_SheetName == '':
            df_data = pd.read_excel(str_path, header=bl_header)
        else:
            df_data = pd.read_excel(str_path, header=bl_header, sheet_name=str_SheetName)
    except Exception as err:
        # version needed: pandas==1.1.4 and xlrd==1.2.0 + change the xlsx file
        logger.warning(' WARNING in pd_read_excel (fl, read_excel) : xlrd did not work, will try with openpyxl')
        logger.warning('  - version needed: xlrd==1.2.0')
        logger.warning('  - And replace the file xlsx.py (/Lib/site-packages/xlrd) by the one in this library !!!')
        logger.warning(
            '  - https://stackoverflow.com/questions/65254535/xlrd-biffh-xlrderror-excel-xlsx-file-not-supported')
        logger.warning('  - |{}|'.format(err))
        try:
            if str_SheetName == '':
                df_data = pd.read_excel(str_path, header=bl_header, engine='openpyxl')
            else:
                df_data = pd.read_excel(str_path, header=bl_header, engine='openpyxl', sheet_name=str_SheetName)
        except Exception as err2:
            logger.error(' ERROR: pd_read_excel (fl)')
            logger.error(' - |{}|'.format(err))
            logger.error(' - |{}|'.format(err2))
            logger.error('  - Path : |{}|'.format(str_path))
            logger.error('  - SheetName : |{}|'.format(str_SheetName))
            logger.error('  - ** ARGS : |{}|'.format(bl_header))
            raise
    return df_data

def fDf_readExcelWithPassword(str_path, str_SheetName, str_ExcelPassword, str_areaToLoad=''):
    """ You can read an Excel file protected with password - Requires to open the Excel App
        Also, for performance issue (and in order not to open Excel App again)
        it will create a csv copy named: fileName_sheetName.csv
        Once the csv created, the same function will only use |pd.read_csv()|
        Return a Dataframe
        """
    # Create the CSV Name
    l_pathCSV = str_path.split('.')
    str_pathCsv = '.'.join(l_pathCSV[:-1]) + '_' + str_SheetName + '.csv'
    # Check if the CSV exists
    if fBl_FileExist(str_pathCsv):
        df_data = pd.read_csv(str_pathCsv, header=0)
    else:
        logger.warning('   [:-)] Saving xls with passwor into a CSV: |{}|'.format(str_pathCsv))
        xl_app = XlsApp.fApp_xls_win32()
        xl_app.define_xls_app()
        xl_app.set_xls_option(True, True, False)
        xl_app.OpenWorkbook(str_path, str_ExcelPassword)
        xl_app.DefineWorksheet(str_SheetName)
        xl_sh = xl_app.xl_lastWsh
        # xlApp = c_win32_xlApp()
        # xlApp.FindXlApp(bl_visible=True)
        # xlApp.xlApp.DisplayAlerts = False
        # xlApp.OpenWorkbook(str_path, str_ExcelPassword)
        # xl_sh = xlApp.DefineWorksheet(str_SheetName, 1)
        if str_areaToLoad == '':
            int_lastRow, int_lastCol = fTup_GetLastRowCol(xl_sh, 1, 1)
            rg_content = xl_sh.Range(xl_sh.Cells(1, 1), xl_sh.Cells(int_lastRow, int_lastCol)).Value
        else:
            logger.warning('   [**] Area To Load: |{}|'.format(str_areaToLoad))
            rg_content = xl_sh.Range(str_areaToLoad).Value
        df_data = pd.DataFrame(list(rg_content))
        df_data = dframe.fDf_Make1stRow_columns(df_data)
        # Create the CSV
        df_data.to_csv(str_pathCsv, index=False, header=True)
        # Close
        xl_app.CloseWorkbook(saveBeforeClose=True)
        xl_app.QuitXlApp(bl_force=False)
    return df_data

def fDic_readExcelWithPassword_sevSh(str_path, str_ExcelPassword, d_shName_areaToLoad={}):
    """ You can read an Excel file protected with password - Requires to open the Excel App
        Also, for performance issue (and in order not to open Excel App again)
        it will create 1 CSV per sheet in the spredsheet named: fileName_sheetName.csv
        Once all the csv created, the same function will only use |pd.read_csv()|
        Return a sictionary of Dataframe, key will be the SheetNames
        """
    d_data = {}
    # Create the CSV Name
    d_pathCsv = {sh: '.'.join(str_path.split('.')[:-1]) + '_' + sh + '.csv' for sh in d_shName_areaToLoad.keys()}
    # Check if the CSV exists
    for shName in d_pathCsv:
        str_pathCsv = d_pathCsv[shName]
        if fBl_FileExist(str_pathCsv):
            df_data = pd.read_csv(str_pathCsv, header=0)
            d_data[shName] = df_data
    # Open Excel and create the CSV if Non Existing
    d_remaining = {k: v for k, v in d_pathCsv.items() if k not in d_data.keys()}
    if d_remaining:
        # Open Excel
        xl_app = XlsApp.fApp_xls_win32()
        xl_app.define_xls_app()
        xl_app.set_xls_option(True, True, False)
        xl_app.OpenWorkbook(str_path, str_ExcelPassword)
        # xl_app = c_win32_xlApp()
        # xl_app.FindXlApp(bl_visible=True)
        # xl_app.xlApp.DisplayAlerts = False
        # xl_app.OpenWorkbook(str_path, str_ExcelPassword)
        # Define Sheet and save Data
        i_sh = 0
        for shName in d_remaining:
            i_sh += 1
            xl_app.DefineWorksheet(shName)
            xl_sh = xl_app.xl_lastWsh
            # xl_sh = xl_app.DefineWorksheet(shName, i_sh)
            str_areaToLoad = d_shName_areaToLoad[shName]
            if str_areaToLoad == '':
                int_lastRow, int_lastCol = fTup_GetLastRowCol(xl_sh, 1, 1)
                rg_content = xl_sh.Range(xl_sh.Cells(1, 1), xl_sh.Cells(int_lastRow, int_lastCol)).Value
            else:
                logger.warning('   [**] Area To Load in sheet |{}|: {}'.format(shName, str_areaToLoad))
                rg_content = xl_sh.Range(str_areaToLoad).Value
            df_data = pd.DataFrame(list(rg_content))
            df_data = dframe.fDf_Make1stRow_columns(df_data)    # Add Header: first Row
            str_firstColumn = list(df_data.columns)[0]          # Remove Empty row
            df_data = dframe.fDf_DropRowsIfNa_resetIndex(df_data, l_colToDropNA=[str_firstColumn])
            str_pathCsv = d_pathCsv[shName]                     # Create the CSV
            df_data.to_csv(str_pathCsv, index=False, header=True)
            d_data[shName] = df_data                    # add in dico
        # CLose
        xl_app.CloseWorkbook(False)
        xl_app.QuitXlApp(bl_force=False)
    return d_data

def fTup_GetLastRowCol(xl_sh, int_rowStart=1, int_colStart=1):
    int_row = int_rowStart
    int_col = int_colStart
    while xl_sh.Cells(int_row, int_colStart).Value != None:
        int_row += 1
    int_lastRow = int_row - 1
    while xl_sh.Cells(int_rowStart, int_col).Value != None:
        int_col += 1
    int_lastCol = int_col - 1
    return int_lastRow, int_lastCol



# -----------------------------------------------------------------
# CREATE XLS Files - ExcelWriter
# -----------------------------------------------------------------
def fStr_createExcel_1Sh(str_folder, str_FileName, df_Data, str_SheetName='', bl_header=False):
    """ Create a single sheet Excel file"""
    try:
        # Define Path
        str_path = fStr_BuildPath(str_folder, str_FileName)
        # Create the File
        if str_SheetName != '':
            df_Data.to_excel(str_path, header=bl_header, index=False, sheet_name=str_SheetName)
        else:
            df_Data.to_excel(str_path, header=bl_header, index=False)
    except Exception as err:
        logger.error('  ERROR: fStr_createExcl_1Sh did not work: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - SheetName : |{}|'.format(str_SheetName))
        return False
    return str_path

def fStr_createExcel_SevSh(str_folder, str_FileName, l_dfData, l_SheetName=[], bl_header=False, d_options={}):
    """ Create a several sheets Excel file
    Input is a list of Dataframe
    Will use pd.ExcelWriter and will no return any error depending of the version of xlrd
    if |options = d_options| wont work, |engine_kwargs = {'options' : d_options}| will be tried as well
    """
    try:
        # Define Path
        str_path = fStr_BuildPath(str_folder, str_FileName)
        # Create the File
        #   Special Treatment for Python > 3.9 (Python 3.11)
        if sys.version_info.major == 3:
            if sys.version_info.minor >= 10:
                try:
                    str_path = fStr_createExl_SevSh_eng_kwarg(str_path, l_dfData, l_SheetName, bl_header, d_options)
                except:
                    str_path = fStr_createExcel_SevSh_options(str_path, l_dfData, l_SheetName, bl_header, d_options)
            else:
                try:
                    str_path = fStr_createExcel_SevSh_options(str_path, l_dfData, l_SheetName, bl_header, d_options)
                except:
                    str_path = fStr_createExl_SevSh_eng_kwarg(str_path, l_dfData, l_SheetName, bl_header, d_options)
        else:
            oth.DisplayMessage_Python3()
            raise
    except Exception as err:
        logger.error('  ERROR: fl fStr_createExcel__SevSh did not work: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - l_SheetName : |{}|'.format('|'.join(l_SheetName)))
        return False
    return str_path

def fStr_createExcel_SevSh_options(str_path, l_dfData, l_SheetName=[], bl_header=False, d_options={}):
    try:
        # options={'strings_to_numbers': True}
        with pd.ExcelWriter(str_path, engine='xlsxwriter', options=d_options) as xl_writer:
            for i in range(len(l_dfData)):
                df_data = l_dfData[i]
                try:
                    str_SheetName = l_SheetName[i]
                except:
                    str_SheetName = 'Sheet{}'.format(str(i + 1))
                df_data.to_excel(xl_writer, header=bl_header, index=False, sheet_name=str_SheetName)
    except Exception as err:
        logger.warning('    WARNING: fl fStr_createExl_SevSh_optons did not work |{}|'.format(err))
        raise
    return str_path

def fStr_createExl_SevSh_eng_kwarg(str_path, l_dfData, l_SheetName=[], bl_header=False, d_options={}):
    '''This function is for newer xlrd version '''
    try:
        with pd.ExcelWriter(str_path, engine='xlsxwriter', engine_kwargs={'options': d_options}) as xl_writer:
            # Dataframe
            for i in range(len(l_dfData)):
                df_data = l_dfData[i]
                # Sheet Name
                try:
                    str_SheetName = l_SheetName[i]
                except:
                    str_SheetName = 'Sheet{}'.format(str(i + 1))
                # fill in
                df_data.to_excel(xl_writer, header=bl_header, index=False, sheet_name=str_SheetName)
    except Exception as err:
        logger.warning('    WARNING: fl fStr_createExl_SevSh_eng_kwarg did not work : |{}|'.format(err))
        raise
    return str_path


# -----------------------------------------------------------------
# INSERT SHEET: 1 file out - 1 Dataframe - 1 Sheet  - ExcelWriter
# -----------------------------------------------------------------
def fStr_fillExcel_InsertNewSheet(str_folder, str_FileName, df_data, str_SheetName='', bl_header=False):
    """ Take an existing  Excel file and insert a new sheet
    Input is a list of Dataframe - Will use pd.ExcelWriter
    """
    if str_FileName == '':      str_path = str_folder
    else:                       str_path = fStr_BuildPath(str_folder, str_FileName)

    if sys.version_info.major == 3:
        if sys.version_info.minor >= 10:
            # Python 3.11 - Pandas 1.5
            str_path = fStr_fillExcel_InsertNewSheet_Py311Pand15(str_path, df_data, str_SheetName, bl_header)
        else:
            # Python 3.9 - Pandas 1.1
            str_path = fStr_fillExcel_InsertNewSheet_Py39Pand11(str_path, df_data, str_SheetName, bl_header)
    else:
        logger.warning('WARNING: do you use a Python 3 ???')
        str_path = fStr_fillExcel_InsertNewSheet_Py39Pand11(str_path, df_data, str_SheetName, bl_header)
    return str_path

def fStr_fillExcel_InsertNewSheet_Py311Pand15(str_path, df_data, str_SheetName = '', bl_header = False):
    try:
        # With
        with pd.ExcelWriter(str_path, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as xl_writer:
            # ---------------------------------------------------------------
            # Manage Sheet Name
            if str_SheetName == '':     str_SheetName = 'Sh1'
            # Rename a sheet because we dont want to replace
            if str_SheetName in list(xl_writer.sheets):
                logger.warning(" The sheet '{}' already exist".format(str_SheetName))
                while str_SheetName in list(xl_writer.sheets):
                    str_SheetName = str_SheetName[1:] + str_SheetName[0] + 'x'
                logger.warning(" We replace the sheet name: '{}'  but you need to improve the management of name".format(str_SheetName))
            # ---------------------------------------------------------------
            # Add the Sheet
            df_data.to_excel(xl_writer, header = bl_header, index = False, sheet_name = str_SheetName)
    except Exception as err:
        logger.error('  ERROR in fl fStr_fillExcel_InsertNewSheet_Py311Pand15: Could not fill the file: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - SheetName : |{}|'.format(str_SheetName))
        return False
    return str_path

def fStr_fillExcel_InsertNewSheet_Py39Pand11(str_path, df_data, str_SheetName = '', bl_header = False):
    try:
        # Define Book
        xl_book = openpyxl.load_workbook(filename=str_path)
        # With
        with pd.ExcelWriter(str_path, mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as xl_writer:
            xl_writer.book = xl_book
            xl_writer.sheets = dict((ws.title, ws) for ws in xl_book.worksheets)
            # ---------------------------------------------------------------
            # ManAge Sheet Name
            if str_SheetName == '':     str_SheetName = 'Sh1'
            if str_SheetName in list(xl_writer.sheets):
                logger.warning(" The sheet '{}' already exist".format(str_SheetName))
                while str_SheetName in list(xl_writer.sheets):
                    str_SheetName = str_SheetName[1:] + str_SheetName[0] + 'x'
                logger.warning(" We replace the sheet name: '{}'  but you need to improve the management of name".format(str_SheetName))
            # ---------------------------------------------------------------
            # Add the Sheet
            df_data.to_excel(xl_writer, header=bl_header, index=False, sheet_name=str_SheetName)
            # SAVE
            xl_writer.save()
    except Exception as err:
        logger.error('  ERROR in fl fStr_fillExcel_InsertNewSheet_Py39Pand11: Could not fill the file: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - SheetName : |{}|'.format(str_SheetName))
        return False
    return str_path

def Act_CopySheetExcel_fomCsv(str_pathWkDest, l_PathWkOrigin, l_SheetName=[]):
    # Loop on the different CSV
    l_sh = []
    for i in range(len(l_PathWkOrigin)):
        str_pathWkOrigin = l_PathWkOrigin[i]
        try:
            try:
                df_data = pd.read_csv(str_pathWkOrigin, header=None)
            except:
                df_data = dframe.fDf_readCsv_enhanced(str_pathWkOrigin, bl_header=None, l_names=range(6))
        except Exception as err:
            logger.error('  ERROR: Could not Take the CSV into DF: |{}|'.format(err))
            logger.error('  - Path : |{}|'.format(str_pathWkOrigin))
            raise
        # Get the sheet Name
        try:
            str_SheetName = l_SheetName[i]
        except:
            str_SheetName = str_pathWkOrigin.split('\\')[-1]
            str_SheetName = str_SheetName.split('.csv')[0]
            str_SheetName = str_SheetName[:15]
            while str_SheetName in l_sh:
                str_SheetName = str_SheetName[:len(str_SheetName - 1)] + '_' + str(i + 1)
            l_sh.append(str_SheetName)
        # Create the XLSX file
        try:
            if fBl_FileExist(str_pathWkDest):
                str_pathReturn = fStr_fillExcel_InsertNewSheet(str_pathWkDest, '', df_data, str_SheetName)
            else:
                str_pathReturn = fStr_createExcel_1Sh(str_pathWkDest, '', df_data, str_SheetName)
        except Exception as err:
            logger.error('  ERROR: Could not create / Fill the XLSX file: |{}|'.format(err))
            logger.error('  - Path Origin : |{}|'.format(str_pathWkOrigin))
            logger.error('  - Path Dest : |{}|'.format(str_pathWkDest))
            logger.error('  - path Return : |{}|'.format(str_pathReturn))
    return True







# -----------------------------------------------------------------
# CREATE XLS Files - Using Excel App
# -----------------------------------------------------------------
# 1 file out - 1 Dataframe - 1 Sheet
def fStr_fillXls_celByCel(str_path, df_data, str_SheetName='', xl_sh=0, int_nbRows=0, int_rowsWhere=1):
    """ Take an existing Excel file and an existing sheet and fill it with new data
    Input is a list of Dataframe - Will use c_win32 xlApp class
    """
    try:
        # If Sheet is nothing, we must define it
        if xl_sh == 0:
            bl_CloseExcel = True
            xl_app = XlsApp.fApp_xls_win32()
            xl_app.define_xls_app()
            xl_app.set_xls_option(True, True, False)
            xl_app.OpenWorkbook(str_path)
            xl_app.DefineWorksheet(str_SheetName)
            xl_sh = xl_app.xl_lastWsh
            if xl_sh == 0:
                logger.warning('  (--) ERROR in fStr_filXls_celByCel: really could not find the sheet')
                raise
        else:   bl_CloseExcel = False
    except Exception as err:
        logger.error('  ERROR in fl fStr_filXls_celByCel: Could not find Excel: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - SheetName : |{}|'.format(str_SheetName))
        return False

    # ------ Insert or delete ROWS ------
    try:
        if int_nbRows > 0:
            for i in range(0, int_nbRows):      xl_sh.Rows(int_rowsWhere).EntireRow.Insert()
        elif int_nbRows < 0:
            for i in range(0, -int_nbRows):     xl_sh.Rows(int_rowsWhere).EntireRow.Delete()
    except Exception as err:
        logger.error('  ERROR in fl fStr_filXls_celByCel, Insert or delete ROWS: |{}|'.format(err))
        try:    logger.error('  - int_nbRows : ', int_nbRows, 'int_rowsWhere: ', int_rowsWhere)
        except: pass
        return False

    # ------ Fill Cell by Cell  ------
    try:
        i_max, j_max = 1, 1
        for i, row in enumerate(df_data.index):
            for j, col in enumerate(df_data.columns):
                xl_sh.Cells(i + 1, j + 1).Value = str(df_data.iat[i, j])
                j_max = j + 1
            i_max = i + 1
    except Exception as err:
        logger.error('  ERROR in fl fStr_filXls_celByCel, Fill Cell by Cell: |{}|'.format(err))
        try:
            logger.error(f'  - i_max= {i_max}, j_max= {j_max}')
            logger.error(f'  - Cell value: {df_data.iat[i, j]}')
        except: pass
        return False

    # Empty the rest of the sheet
    try:
        col =   XlsFmt.fDic_colNumber()[j_max]
        range = f"A{i_max + 1}:B{col}{i_max + 1000}"
        xl_sh.Range(range).ClearContents()
    except Exception as err:
        logger.error('  ERROR in fl fStr_filXls_celByCel: Empty the rest of the sheet: |{}|'.format(err))
        try:
            logger.error(f'  - i_max= {i_max}, j_max= {j_max}')
            logger.error(f'  - col= {col}')
            logger.error(f'  - range= {range}')
        except: pass
        return False

    # rustine depending where Function start
    if bl_CloseExcel:
        try:                        xl_app.CloseWorkbook(True)
        except Exception as err:    logger.error('  ERROR in fl fStr_filXls_celByCel: Excel workbook could not be closed | {}'.format(str(err)))
        try:                        xl_app.QuitXlApp()
        except Exception as err:    logger.error('  ERROR: Excel could not be closed | {}'.format(str(err)))
    return str_path


# 1 file out - n Dataframe - n Sheet
def fStr_fillXls_celByCel_plsSheets(str_folder, str_FileName, l_dfData, l_SheetName=[], l_nbRows=[], l_rowsWhere=[]):
    try:
        if str_FileName == '':
            str_path = str_folder
        else:
            str_path = fStr_BuildPath(str_folder, str_FileName)
        # Open the file (win32)
        xl_app = XlsApp.fApp_xls_win32()
        xl_app.define_xls_app()
        xl_app.set_xls_option(False, False, False)
        xl_app.OpenWorkbook(str_path)
        # Dataframe
        for i in range(len(l_dfData)):
            df_data = l_dfData[i]
            try:    str_SheetName = l_SheetName[i]
            except: str_SheetName = ''
            # Sheet
            xl_app.DefineWorksheet(str_SheetName)
            # ------ Insert or delete ROWS ------
            int_nbRows = 0
            int_rowsWhere = 1
            if l_nbRows:
                try:
                    int_nbRows = l_nbRows[i]
                except:
                    int_nbRows = 0
                try:
                    int_rowsWhere = l_rowsWhere[i]
                except:
                    int_rowsWhere = 1
            # FILL THE SHEET
            fStr_fillXls_celByCel(str_path, df_data, str_SheetName, xl_app.xl_lastWsh, int_nbRows, int_rowsWhere)
        # Visible and close Excel at the end
        xl_app.set_xls_option()
        xl_app.CloseWorkbook(True)
        xl_app.QuitXlApp()
    except Exception as err:
        try:    xl_app.CloseWorkbook(True)
        except: logger.error('  ERROR in fillXls_celByCel_plsSheets: Excel workbook could not be closed')
        try:    xl_app.QuitXlApp()
        except: logger.error('  ERROR: Excel could not be closed')
        logger.error('  ERROR in fStr_fillXls_celByCel plsSheets: Could not create the PCF: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        return False
    return str_path


# 1 file out - 1 Dataframe - 1 Sheet
def fStr_fillXls_df_xlWgs(str_path, df_data, str_SheetName='', xl_sheet=0, int_nbRows=0, int_rowsWhere=1):
    """ Take an existing Excel file and an existing sheet and fill it with new data
    Input is a Dataframe - Will use c_xlApp xlwings class"""
    try:
        xl_app = XlsApp.fApp_xls_wings()

        # If Sheet is nothing, we must define it
        if xl_sheet == 0:
            bl_CloseExcel = True
            xl_app.define_xls_app()
            xl_app.set_xls_option(True, False, False)
            xl_app.OpenWorkbook(str_path)
            xl_app.DefineWorksheet(str_SheetName)
            xl_sheet = xl_app.xl_lastWsh
            if not xl_sheet:        logger.warning(
                '  (--) ERROR in fStr_filXls_celByCel: really could not find the sheet')
        else:
            # We do not close the workbook if we need to fill several Sheet
            bl_CloseExcel = False
            xl_app.xl_lastWk = xl_sheet

        # ------ Insert or delete ROWS ------
        if int_nbRows > 0:
            for i in range(0, int_nbRows):      xl_sheet.range("{0}:{0}".format(str(int_rowsWhere))).api.Insert()
        elif int_nbRows < 0:
            for i in range(0, -int_nbRows):     xl_sheet.range("{0}:{0}".format(str(int_rowsWhere))).api.Delete()
        # ------ Fill DF------
        xl_app.InsertDf_inRange(df_data)
        # Close if only one sheet
        if bl_CloseExcel:
            try:
                xl_app.CloseWorkbook(saveBeforeClose=True)
                xl_app.QuitXlApp()
            except Exception as err: logger.error(f'  ERROR in fl fStr_filXls_df_xlWgs: close Book | {err}')
    except Exception as err:
        logger.error('  ERROR in fl fStr_filXls_df xlWgs | {}'.format(str(err)))
        logger.error('  - Path : |{}|'.format(str_path))
        logger.error('  - SheetName : |{}|'.format(str_SheetName))
        logger.error('  - ** ARGS : |{}|-|{}|'.format(str(int_nbRows), str(int_rowsWhere)))
        xl_app.set_xls_option(True, True, True)
        return False
    return str_path


# # 1 fileout - n Dataframe - n Sheet
def fStr_fillXls_df_xlWgs_sevSh(str_folder, str_FileName, l_dfData, l_SheetName=[], l_nbRows=[], l_rowsWhere=[]):
    """ Take an existing Excel file and several existing sheet and fill it with new data
    Input is a list of Dataframe, SheetNames - Will use c_xlApp xlwings class"""
    try:
        str_path = fStr_BuildPath(str_folder, str_FileName)
        xl_app = XlsApp.fApp_xls_wings()
        xl_app.define_xls_app()
        xl_app.set_xls_option(True, False, False)
        xl_app.OpenWorkbook(str_path)
        # Dataframe
        for i in range(len(l_dfData)):
            df_data = l_dfData[i]
            try:
                str_SheetName = l_SheetName[i]
            except:
                str_SheetName = ''
            # Sheet
            xl_app.DefineWorksheet(str_SheetName)
            # ------ Insert or delete ROWS ------
            int_nbRows = 0
            int_rowsWhere = 1
            if l_nbRows:
                try:
                    int_nbRows = l_nbRows[i]
                except:
                    int_nbRows = 0
                try:
                    int_rowsWhere = l_rowsWhere[i]
                except:
                    int_rowsWhere = 1
            # FILL THE SHEET
            fStr_fillXls_df_xlWgs(str_path, df_data, str_SheetName, xl_app.xl_lastSheet, int_nbRows, int_rowsWhere)
        # Close Wk
        xl_app.CloseWorkbook(saveBeforeClose=True)
        xl_app.QuitXlApp()
    except Exception as err:
        logger.error('  ERROR in fStr_fillXls_df_xlWgs_sevSh: Could not create the PCF: |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_path))
        xl_app.set_xls_option(True, True, True)
        return False
    return str_path



#==============================================================================
# Merge XLS workbook - COPY SHEET - 1 file out - several Sheet
#==============================================================================
def fStr_fillExcel_MergeWk_CopySh(str_pathDest, l_wkToMerge = [], bl_header = None, bl_formatCopySheetXls = False):
    """ Take a list of Workbook (path)
    Copy the first input WK into destination (path)
    Copy sheet by sheet into Dest for the rest
        - Value / DF (Will use pd.ExcelWriter)
        - with Format (will use class c_xlApp xlwings)
    """
    try:
        # 0. If the list of Workbook is empty
        if l_wkToMerge == []:
            logger.error('ERROR: fStr_fillExcel_MergeWk_Copyh, no workbook defined in l_wkToMerge')
            return False
        # 1. Copy-Paste the first Workbook
        str_pathFileInitial = l_wkToMerge[0]
        shutil.copyfile(str_pathFileInitial, str_pathDest)
        # 2. End if its just one Workbook (then its over)
        if len(l_wkToMerge) <= 1:
            logger.warning('INFO: fStr_fillEx_MergeWk_Copy, l_wkToMerge had only 1 workbook...')
            logger.warning('  ... That will work but the function is made for merging Excel WK')
            return str_pathDest
    except Exception as err:
        logger.error('ERROR 1 fStr_fillExcel_MergeWk_Copyh || {} '.format(err))
        raise

    # 3. Loop on the other workbook to check the sheet to add up
    try:
        # List the Sheet in the first file we copied ealier => to extend the final list of Sheets
        l_sheetDest = fL_getSheetName_xls(str_pathFileInitial)
        d_sheetToMerge = {}
        for _exlWk in l_wkToMerge[1:]:
            # List the Sheet in the Workbook to merge
            l_sheetToMerge = fL_getSheetName_xls(_exlWk)
            # Tell which sheet is already in the destination
            l_common = [sh for sh in l_sheetToMerge if sh in l_sheetDest]
            if len(l_common) > 0:
                logger.warning('\n  (**) WARNING: The destination workbook already contain the sheet you try to merge:')
                logger.warning(' -'.join(l_common))
                logger.warning('')
                l_sheetToMerge = [sh for sh in l_sheetToMerge if sh not in l_sheetDest]
                d_sheetToMerge[_exlWk] = l_sheetToMerge
            else:
                d_sheetToMerge[_exlWk] = True
            # Extend the list of Total Sheet => Add up the new sheet in the destination
            l_sheetDest.extend(l_sheetToMerge)
    except Exception as err:
        logger.error('ERROR 3 pp.fStr_fillEx_MergeWk_Copy || {} '.format(err))
        raise

    # 4. if format is needed, we need to use EXCEL APP
    if bl_formatCopySheetXls is True:
        try:
            xl_app = XlsApp.fApp_xls_wings()
            xl_app.define_xls_app()
            xl_app.set_xls_option(True, False, False)
            for _exlWk in l_wkToMerge[1:]:
                l_sheetToMerge = d_sheetToMerge[_exlWk]
                # If it's True, it means, we take all the sheet
                if l_sheetToMerge is True:
                    xl_app.CopySheetFromAnotherBook(_exlWk, str_pathDest=str_pathDest, bl_allSheets=True)
                else:
                    xl_app.CopySheetFromAnotherBook(_exlWk, str_pathDest=str_pathDest, shName=l_sheetToMerge)
            # Quit the APP - NO RAISE ERROR...
            try:
                xl_app.Quit_xlApp()
            except Exception as err:
                logger.error('ERROR 4b fStr_fillEx_MergeWk Copy - Quit App || {} '.format(err))
        except Exception as err:
            logger.error('ERROR 4a fStr_fillEx_MergeWk Copy || {} '.format(err))
            raise
    # 5. if only value needed, lets just use pandas.ExcelWriter / openxyl to add the sheet
    else:
        try:
            # Remove the openxyl warnings
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                with pd.ExcelWriter(str_pathDest, mode='a', engine='openpyxl', if_sheet_exists='replace') as xl_writer:
                    for _exlWk in l_wkToMerge[1:]:
                        l_sheetToMerge =    d_sheetToMerge[_exlWk]
                        # If its True, it means, we take all the sheet
                        if l_sheetToMerge is True:
                            l_sheetToMerge = pd.ExcelFile(_exlWk).sheet_names
                        # Loop on all the sheets
                        for _shName in l_sheetToMerge:
                            # Get the dataframe from input
                            df_data =       pd_read_excel(_exlWk, str_SheetName = _shName, bl_header = bl_header)
                            # Write it to a sheet in the output excel
                            df_data.to_excel(xl_writer, sheet_name = _shName, index = False, header = bl_header)
        except Exception as err:
            logger.error('ERROR 4c pp.fStr_fillEx_MergeWk_Copy || {} '.format(err))
            raise
    return str_pathDest


# -----------------------------------------------------------------
# CONVERT XLS File
# -----------------------------------------------------------------
# TODO: Factorize, they seem to be all the same function
def fDf_convertToXlsx(str_path, str_SheetName='', bl_header=None):
    """ Will use Act_win32_SaveAsCleanFile to make sure the file is not corrupted
    and SaveAs XLSX instead of XLS
    Read it and return the dataframe """
    if '.xlsx' == str_path.lower()[-5:]:
        str_pathNew = str_path
    else:
        str_pathNew = str_path.replace('.xls', '.xlsx').replace('.XLS', '.xlsx')
        # Open Excel and Save as a XLSX version
    Act_win32_SaveAsCleanFile(str_path, str_pathNew)
    # Read the file
    df_data = pd_read_excel(str_pathNew, str_SheetName, bl_header)
    return df_data

def fDf_overwriteXlsx(str_path, str_SheetName='', bl_header=None):
    """ Will use Act_win32_SaveAsCleanFile to save a non-corrupted XLSX file
    Read it and return the dataframe """
    str_pathNew = str_path.replace('.xlsx', '_clean.xlsx').replace('.XLSX', '_clean.xlsx')
    # Open Excel and Save as a XLSX version
    Act_win32_SaveAsCleanFile(str_path, str_pathNew)
    # Read the file
    df_data = pd_read_excel(str_pathNew, str_SheetName, bl_header)
    return df_data

def Act_convertToXls_fromXlsx(str_path):
    """ Will use Act_win32_SaveAsCleanFile to make sure the file is not corrupted
    and SaveAs XLS instead of XLSX """
    str_pathNew = str_path.replace('.xlsx', '.xls').replace('.XLSX', '.xls')
    # Open Excel and Save as a XLSX version
    logger.warning('  (*) Copying XLSX file into XLS: {} \n'.format(str_pathNew.split('Auto_py')[-1]))
    Act_win32_SaveAsCleanFile(str_path, str_pathNew)

def Act_win32_SaveAsCleanFile(str_path, str_pathNew):
    """ Sometimes an Excel file is an old version and might be corrupted
    By Passing your file through this function, Excel App will be open, SaveAs and Close so the new File will be useable"""
    # Test if file exist
    if not fBl_FileExist(str_pathNew):
        try:
            xl_app = XlsApp.fApp_xls_win32()
            xl_app.define_xls_app()
            xl_app.set_xls_option(True, True, False)
            xl_app.OpenWorkbook(str_path)
            xl_app.SaveBook(str_newPath=str_pathNew, int_fileFormat=51)
            xl_app.CloseWorkbook(saveBeforeClose=False)
            # that was not in the version py2Nut 4.
            xl_app.QuitXlApp()
        except Exception as err:
            logger.error('  ERROR: Act_win32_SaveAsCleanFile: |{}|'.format(err))
            logger.error('  - Path : |{}|'.format(str_path))
            raise
    return True

def Act_win32OConvertXls_pdf(str_path):
    """ Will open an Excel file and convert it into PDF"""
    logger.warning('  (*) Converting XLSX file into PDF: {} \n'.format(str_path.split('Auto_py')[-1]))
    if not fBl_FileExist(str_path.replace('.xlsx', '.pdf')):
        try:
            xl_app = XlsApp.fApp_xls_win32()
            xl_app.define_xls_app()
            xl_app.set_xls_option(True, True, False)
            xl_app.OpenWorkbook(str_path)
            xl_app.ConvertToPdf()
            xl_app.CloseWorkbook(saveBeforeClose=False)
            # that was not in the version py2Nut 4.
            xl_app.QuitXlApp()
        except Exception as err:
            logger.error('  ERROR: Act_win32_SaveAsCleanFile: |{}|'.format(err))
            logger.error('  - Path : |{}|'.format(str_path))
            raise
        return True


# -----------------------------------------------------------------
# Other Quick Launcher - TODO: Replace in the code by direct link to the file
# -----------------------------------------------------------------
def Act_win32OpenSaveXls(str_path):
    xl_app = XlsApp.fApp_xls_win32()
    xl_app.define_xls_app()
    xl_app.set_xls_option(True, True, False)
    xl_app.OpenWorkbook(str_path)
    xl_app.CloseWorkbook(saveBeforeClose=True)
    # that was not in the version py2Nut 4.
    xl_app.QuitXlApp()
    return True

def OpenSaveXls_xlWing(str_path):
    xl_app = XlsApp.fApp_xls_wings()
    xl_app.define_xls_app()
    xl_app.set_xls_option(True, False, False)
    xl_app.OpenWorkbook(str_path)
    xl_app.CloseWorkbook(saveBeforeClose=True)
    # that was not in the version py2Nut 4.
    xl_app.QuitXlApp()
    return True

def fApp_xls_win32():
    # to replace AppXls_win32 by this in seita
    return XlsApp.fApp_xls_win32()
def fApp_xls_wings():
    # to replace c_xlApp_xlwings by this in seita
    return XlsApp.fApp_xls_wings()

def Act_KillExcel():
    return flCopy.Act_KillExcel()
def c_copyPaste():
    return flCopy.c_copyPaste()
def copyPaste_shutil(*args, **kwargs):
    return flCopy.copyPaste_shutil(*args, **kwargs)
def fL_GetListSubFolder_except(*args, **kwargs):
    return flCopy.fL_GetListSubFolder_except(*args, **kwargs)
def fL_GetListDirFileInFolders(*args, **kwargs):
    return flCopy.fL_GetListDirFileInFolders(*args, **kwargs)
def Act_CopyUpdateFiles_specialBackUp(*args, **kwargs):
    return flCopy.Act_CopyUpdateFiles_specialBackUp(*args, **kwargs)
def fStr_CopPasteFolder(*args, **kwargs):
    return flCopy.fStr_CopPasteFolder(*args, **kwargs)
def Act_CopPasteFolder_severalTry(*args, **kwargs):
    return flCopy.Act_CopPasteFolder_severalTry(*args, **kwargs)

def Act_StyleIntoExcel(*args, **kwargs):
    return XlsFmt.Act_StyleIntoExcel(*args, **kwargs)
