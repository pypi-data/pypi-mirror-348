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
oth =       lib.nutOther()
dat =       lib.nutDate()
dframe =    lib.nutDataframe()
fl =        lib.nutFiles()
logger =    lib.logger()
xlsxwriter = lib.xlsxwriter()
shutil =    lib.shutil()


# ------------------------------------------------------------------------------
# DEPRECATED - Just for info
# ------------------------------------------------------------------------------
def del_Gen_py_folder(self, str_function):
    # =====================================================
    # Documentation on the subject:
    # https://gist.github.com/rdapaz/63590adb94a46039ca4a10994dff9dbe
    # https://stackoverflow.com/questions/47608506/issue-in-using-win32com-to-access-excel-file/47612742
    # =====================================================
    str_DirPath = fl.fStr_BuildPath(os.environ['USERPROFILE'], r'AppData\Local\Temp\gen_py')
    logger.warning('   (***) delete folder : {}'.format(str_DirPath))
    if fl.fBl_FolderExist(str_DirPath):
        # Delete the folder
        shutil.rmtree(str_DirPath, ignore_errors=True)
    # Re- Launch Process
    if str_function == 'FindXlApp':
        # Define again the App
        xlApp = win32.Dispatch('Excel.Application')
        self.xlApp = xlApp
        return self.xlApp
    #### CALL
    # except AttributeError as err_att:
    #     if "no attribute 'CLSIDToClassMap'" in str(err_att):
    #         logger.error('  WARNING in FindXlApp: no attribute CLSIDToClassMap || {}'.format(str(err_att)))
    #         self.del_Gen_py_folder('FindXlApp')
    #         return self.xlApp
    #     else:
    #         logger.error('  ERROR in FindXlApp || {}'.format(str(err_att)))
    #         raise


def fStr_createExcel_SevSh_celByCel(str_folder, str_FileName, l_dfData, l_SheetName=[]):
    """ Create a several sheets Excel file
    Input is a list of Dataframe and list of Sheet Names
    Will use xlsxwriter and fill the Excel Cell by Cell
    Performance may be pretty low
    Preferable to use the function : fStr_createExcel_SevSh
    """
    try:
        # Define Path
        if str_FileName == '':
            str_path = str_folder
        else:
            str_path = fStr_BuildPath(str_folder, str_FileName)
        # Create the file (xlsxwriter cannot modify files)
        xlWb = xlsxwriter.Workbook(str_path)
        # Dataframe
        for i in range(len(l_dfData)):
            df_data = l_dfData[i]
            try:
                str_SheetName = l_SheetName[i]
            except:
                str_SheetName = ''
            # Sheet Name
            if str_SheetName != '':
                xlWs = xlWb.add_worksheet(str_SheetName)
            else:
                xlWs = xlWb.add_worksheet()
            # fill in
            for i, row in enumerate(df_data.index):
                for j, col in enumerate(df_data.columns):
                    xlWs.write(i, j, str(df_data.iat[i, j]))
                    # xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
        xlWb.close()
    except Exception as err:
        logger.error('  ERROR: fl fStr__createExcel_SevSh_celByCel did not work : |{}|'.format(err))
        logger.error('  - Path : |{}|'.format(str_folder))
        logger.error('  - fileName : |{}|'.format(str_FileName))
        logger.error('  - l_SheetName : |{}|'.format('|'.join(l_SheetName)))
        try:
            xlWb.close()
        except:
            logger.error('  *** Could not close the file')
        return False
    return str_path