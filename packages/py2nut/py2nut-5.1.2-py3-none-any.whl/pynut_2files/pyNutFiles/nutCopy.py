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
fl =        lib.nutFiles()
# Other
logger =    lib.logger()
shutil =    lib.shutil()
psutil =    lib.psutil()
win32 =     lib.win32()
import os
import datetime as dt
fStr_Message = oth.fStr_Message



# TODO: replace all function in here in Seita


# ---------------------------------------------------------------
# KILL Excel Management (outside of below class)
# ---------------------------------------------------------------
def Act_KillExcel():
    """ This function kills all session of Excel
    Including the 'ghost' session you would kill from the Task Manager """
    try:
        for proc in psutil.process_iter():
            if any(procstr in proc.name() for procstr in ['Excel', 'EXCEL', 'excel']):
                proc.kill()
    except Exception as err:
        logger.error('  ERROR: could not kill EXCEL : |{}|'.format(err))
        logger.error('  - Proc Name : |{}|'.format(proc.name()))
        Act_KillExcel2()

def Act_KillExcel2():
    o_WbemScripting =   win32.Dispatch("WbemScripting.SWbemLocator")
    o_cimv2 =           o_WbemScripting.ConnectServer(".", "root\cimv2")
    o_excelProcess =    o_cimv2.ExecQuery('Select Caption from Win32_Process where Caption LIKE \'EXCEL%\'')
    for excel in o_excelProcess:
        try:
            excel.terminate()
        except:
            logger.error('  ERROR Act_KillExcl2: could not kill EXCEL : |{}|'.format(err))


# -----------------------------------------------------------------
# Copy / Paste
# -----------------------------------------------------------------
@oth.dec_singletonsClass
class c_copyPaste:
    # # Descriptor
    # __slots__ = 'l_path', 'str_rootfolder'
    def __init__(self):
        self.l_path = {}
        self.str_rootfolder = ''

    def copy(self, str_rootfolder='', l_path=[]):
        if l_path and str_rootfolder != '':
            l_pastP = self.l_path
            l_path = [fl.fStr_BuildFolder_wRoot(path, str_rootfolder) for path in l_path]
            try:
                if l_pastP:
                    l_path = l_path + l_pastP
            except Exception as err:
                logger.error('  ERROR : IN.cCopyPaste: could not concat list anymore : |{}|'.format(err))
            finally:
                l_path = list(set(l_path))
                self.l_path = l_path
                self.str_rootfolder = str_rootfolder
        # return True

    def paste(self, str_newRoot=''):
        try:
            if str_newRoot != '':
                l_path = self.l_path
                str_rootfolder = self.str_rootfolder
                l_newP = [path.replace(str_rootfolder, str_newRoot) for path in l_path]
                for (path, newPath) in zip(l_path, l_newP):
                    str_newFolder = fl.fStr_GetFolderFromPath(newPath)
                    # Create Folder if needed and copy paste
                    fl.fBl_createDir(str_newFolder)
                    logger.warning('COPY file...  {} |==>| {}'.format(fl.fStr_GetFileFromPath(path), str_newFolder))
                    copyPaste_shutil(path, newPath)
            else:
                logger.warning(' WARNING in copyPaste: Root Folder to go Paste is not filled ')
        except:
            raise
        finally:
            self.l_path = []
        # return True

def copyPaste_shutil(str_pathOrigin, str_pathDest):
    try:
        shutil.copy(str_pathOrigin, str_pathDest)
        # shutil.copyfile
    except Exception as err:
        logger.error('  ERROR in copyPaste_shutil: {}'.format(err))
        raise
    return True


# ------------------------------------------------------------------------------
# --------- Deliver Files to Archives / Prod --------------
# ------------------------------------------------------------------------------
def fL_GetListSubFolder_except(str_folder, str_folderExcept=''):
    if str_folderExcept != '':
        return [x[0] for x in os.walk(str_folder) if x[0][:9] != str_folderExcept]
    else:
        return [x[0] for x in os.walk(str_folder)]

def fL_GetListDirFileInFolders(l_subDir, l_typeFile=[]):
    listTuple_PathFic = []
    if l_typeFile:
        for Dir in l_subDir:
            list_fic = [(Dir, fic) for fic in fl.fList_FileInDir(Dir) if
                        fic[-3:].lower() in l_typeFile or fic[-4:].lower() in l_typeFile]
            if list_fic: listTuple_PathFic += list_fic
    else:
        for Dir in l_subDir:
            list_fic = [(Dir, fic) for fic in fl.fList_FileInDir(Dir)]
            if list_fic: listTuple_PathFic += list_fic
    return listTuple_PathFic

def Act_CopyUpdateFiles_specialBackUp(l_FolderFic_from, str_DestFolder, dte_after=10, str_removeInDestFolder=''):
    str_message = ''

    # Date limite
    if type(dte_after) == int:
        dte_after = dt.datetime.now() - dt.timedelta(dte_after)

    # Get list of Origin Files
    l_pathOrigin = [fl.fStr_BuildPath(str_folder, str_file) for (str_folder, str_file) in l_FolderFic_from]
    l_pathOrigin_wLimit = fl.fL_KeepFiles_wTimeLimit(l_pathOrigin, dte_after)

    # Create the Folder Destination
    try:
        l_folderDest = [fl.fStr_GetFolderFromPath(str_path).replace('.', str_DestFolder, 1).replace(str_removeInDestFolder,
                                                                                                 '') for str_path in
                        l_pathOrigin_wLimit]
        l_folderDest_unique = list(set(l_folderDest))
        for folder in l_folderDest_unique:
            fl.fBl_createDir(folder)
    except Exception as err:
        str_message += fStr_Message(' ERROR in Act_CopyUpdateFiles_specialBackUp: could not create folder dest ||| {}'.format(folder))
        logger.error(err[:100])
        return str_message

    # Get the Destination Path
    l_pathDest = [str_path.replace('.', str_DestFolder, 1).replace(str_removeInDestFolder, '') for str_path in
                  l_pathOrigin_wLimit]

    # Loop on File to copy / update them
    for i_it in range(len(l_pathOrigin_wLimit)):
        str_pathOrigin = l_pathOrigin_wLimit[i_it]
        str_pathDest = l_pathDest[i_it]
        # If File DOES NOT Exists
        if not fl.fBl_FileExist(str_pathDest):
            str_message += fStr_Message(
                'COPY...  Origin: {} ||| Dest: {}'.format(str_pathOrigin, fl.fStr_GetFolderFromPath(str_pathDest)))
            try:
                shutil.copy(str_pathOrigin, str_pathDest)
            except:
                str_message += fStr_Message(' (--) ERROR: file could not be Copied !!!')
        else:
            # Compare Date (Update only if CLoud is more recent)
            dte_lastmod = fl.fDte_GetModificationDate(str_pathOrigin)
            dte_lastmod_dest = fl.fDte_GetModificationDate(str_pathDest)
            if dte_lastmod > dte_lastmod_dest:
                str_message += fStr_Message(
                    'UPDATE...  Origin: {} ||| Dest: {}'.format(str_pathOrigin, fl.fStr_GetFolderFromPath(str_pathDest)))
                # ---ARCHIVES--------------
                if r'\Archive' in str_DestFolder[-10:]:
                    str_dateTime = str(dte_lastmod_dest.strftime('%Y%m%d'))
                    shutil.copyfile(str_pathDest, fl.fStr_GetFolderFromPath(
                        str_pathDest) + '\\' + str_dateTime + '_' + fl.fStr_GetFileFromPath(str_pathDest))
                # ------------------------
                try:
                    shutil.copy(str_pathOrigin, str_pathDest)
                except:
                    str_message += fStr_Message(' (--) ERROR: file could not be Updated !!!')
    str_message += fStr_Message(' ... End CopyPaste Process !!!')
    return str_message

def fStr_CopPasteFolder(str_folderOrigin, str_folderTarget, dte_after=10, l_typeFile=[], str_folderExcept='',
                        l_fileExcept=[]):
    # Date limite
    if type(dte_after) == int:
        dte_after = dt.datetime.now() - dt.timedelta(dte_after)

    # Environment of work
    dir_current = os.getcwd()
    os.chdir(str_folderOrigin)
    # Get all the sub Dir in the folder -- Except the folder (if empty, no exception)
    l_SubDir_Origin = fL_GetListSubFolder_except('.', str_folderExcept)
    # Get Tuples in List (Path, File Python)
    l_PathFic = fL_GetListDirFileInFolders(l_SubDir_Origin, l_typeFile)
    # Filter out
    if l_fileExcept:
        for _fileExcept in l_fileExcept:
            l_PathFic = [(Dir, fic) for (Dir, fic) in l_PathFic if _fileExcept not in fic]
    # Copy / Update files from a list of tuple to another
    str_message = Act_CopyUpdateFiles_specialBackUp(l_PathFic, str_folderTarget, dte_after)
    # Fin !!
    os.chdir(dir_current)
    return str_message

def Act_CopPasteFolder_severalTry(str_folderDest, l_pathOrigin, dte_after=10, l_typeFile=[], str_folderExcept='',
                                  l_fileExcept=[]):
    for pathOrigin in l_pathOrigin:
        try:
            fStr_CopPasteFolder(pathOrigin, str_folderDest, dte_after=dte_after,
                                l_typeFile=l_typeFile,
                                str_folderExcept=str_folderExcept,
                                l_fileExcept=l_fileExcept)
            return True
        except:
            pass
    return False





# ------------------------------------------------------------------------------
# DEPRECATED - Just for info
# ------------------------------------------------------------------------------

# def Act_CopyUpdateFiles(l_PathFic_from, l_PathFic_dest, str_DestFolder='', str_removeInDestFolder=''):
#     msg = Act_CopyUpdateFiles_specialBackUp(l_PathFic_from, str_DestFolder, dte_after=900,
#                                             str_removeInDestFolder=str_removeInDestFolder)
#     if 'ERROR' in msg:
#         raise
#     return True
