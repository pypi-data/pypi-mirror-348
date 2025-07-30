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
# oth = lib.nutOther()
# dat = lib.nutDate()
# dframe = lib.nutDataframe()
# Other
openpyxl_Excel =    lib.openpyxl_Excel()
PageSetupProperties = lib.PageSetupProperties()
styl =              lib.openpyxl_styles()
logger =            lib.logger()
import os, sys
import time
import datetime as dt
import warnings



# TODO: replace all function in here in Seita



# -----------------------------------------------------------------
# FORMAT / STYLE
# -----------------------------------------------------------------
def Act_StyleIntoExcel(str_path, str_format='', str_SheetName=''):
    """ Take an Excel Spreadsheet and a sheet and apply a format to it
    str_format is a dictionary within a string,
    the dictionary will be built by the fucntion eval
    Example of format:
        "{'A1:M500':{'font':{'name':'Calibri', 'size':9}},
        'B3:B5':{'font':{'name':'Calibri', 'size':10, 'bold':True,'color':styl.colors.WHITE},
                'alignment':{'horizontal':'right'},
                'fill':{'patternType':'solid', 'fill_type':'solid', 'fgColor': 'F2F2F2'}},
        'Column_size':{'A':50,'B':35,'C':10,'D':10,'E':15,'F':15,'G':18,'H':10},
        'Table_bord':{'A3:A11':'normBlack', 'B3:B11':'normBlack'},
        'Table_bord_full':{'A1:B1':'normBlack'},
        'Table_bord_EndDown_full':{'A13':'normBlack'},
        'num_format':{'B6:B6':'#,##0.0000', 'B7:B8':'#,##0'},
        'num_format_col':{'G13':'#,##0.00',  'H13':'0.00%'}
        }"
    """
    # EVAL
    try:
        if str_format == '':    return True
        d_format = eval(str_format)
    except Exception as err:
        logger.error(' ERROR Act_StyleIntoExcl - EVAL: |{}|'.format(err))
        logger.error(str_format)
        return False
    # Define EXCEL objects
    try:
        xlWb = openpyxl_Excel.load_workbook(filename=str_path)
        if str_SheetName == '':
            xlWs = xlWb.active
        else:
            xlWs = xlWb[str_SheetName]
    except Exception as err:
        logger.error(' ERROR Act_StyleIntoExcl, could not define the sheet: |{}|'.format(err))
        return False
    # Launch the different process included into the dico
    try:
        for str_area, d_formatValue in d_format.items():
            if 'column_size' in str_area.lower():
                Act_resizeRowColumn(xlWs, 'column', d_formatValue)
            elif 'row_size' in str_area.lower():
                Act_resizeRowColumn(xlWs, 'row', d_formatValue)
            elif 'Table_bord'.lower() in str_area.lower():
                str_keyType = str_area  # Area is now Table_bord / Table_bord_endDown....
                bl_full, bl_row = False, False
                if '_full' in str_keyType.lower():
                    bl_full = True
                elif '_row' in str_keyType.lower():
                    bl_row = True
                d_border = d_format[str_keyType]
                for str_areaBorder, str_borderName in d_border.items():
                    # If we see a below Array, we need to fund the address of the next Array
                    if 'below_array' in str_areaBorder.lower():
                        str_areaBorder = fStr_FindArea_NextArray(xlWs, str_areaBorder)
                    if '_EndDown'.lower() in str_keyType.lower():
                        rg_toSelect = fRg_SelectRangeToApplyFormat(xlWs, str_areaBorder, bl_includeHeader=True)
                    else:
                        rg_toSelect = xlWs[str_areaBorder]
                    Act_loopBorder(str_keyType, rg_toSelect, str_borderName, bl_full=bl_full, bl_row=bl_row)
            elif 'num_format' in str_area.lower():
                str_keyType = str_area  # Area is now num_format
                d_colParam = d_format[str_keyType]
                for str_areaFormat, str_format in d_colParam.items():
                    # If we see a below Array, we need to fund the address of the next Array
                    if 'below_array' in str_areaFormat.lower():
                        str_areaFormat = fStr_FindArea_NextArray(xlWs, str_areaFormat)
                    if '_col' in str_keyType.lower():
                        rg_toSelect = fRg_SelectRangeToApplyFormat(xlWs, str_areaFormat, bl_includeHeader=False,
                                                                   bl_column=True)
                    else:
                        rg_toSelect = xlWs[str_areaFormat]
                    Act_loopFormat(rg_toSelect, str_format, 'num_format')
            elif 'print_format' in str_area.lower():
                Act_reshapePrintFormat(xlWs, d_formatValue)
            # elif 'below_array' in str_area.lower():
            #     int_skipBelow =     int(str_area.split('-')[1])
            #     str_areaStart =     str_area.split('-')[2]
            #     str_areaEnd =       fRg_FindCellDown(xlWs, str_areaStart, int_skipBelow)
            #     # Classic Selection
            #     str_styleName = fStr_defineStyle(xlWb, d_formatValue)
            #     if ':' in str_areaEnd:  rg_toSelect = xlWs[str_areaEnd]
            #     else:                   rg_toSelect = fRg_SelectRangeToApplyFormat(xlWs, str_areaEnd, bl_includeHeader = True)
            #     Act_loopFormat(rg_toSelect, str_styleName)
            # Classic format where first Key is a Range of Cells
            else:
                str_styleName = fStr_defineStyle(xlWb, d_formatValue)
                # If we see a below Array, we need to fund the address of the next Array
                if 'below_array' in str_area.lower():
                    str_area = fStr_FindArea_NextArray(xlWs, str_area)
                # Define Aera if we just put one cell as input
                if ':' in str_area:
                    rg_toSelect = xlWs[str_area]
                else:
                    rg_toSelect = fRg_SelectRangeToApplyFormat(xlWs, str_area, bl_includeHeader=True)
                Act_loopFormat(rg_toSelect, str_styleName)
    except Exception as err:
        logger.error(' ERROR Act_StyleIntoExcl: Loop on Area for Style : |{}|'.format(err))
    # SAVE
    try:
        xlWb.save(filename=str_path)
    except Exception as err:
        logger.error(' ERROR Act_StyleIntoExcl, xlWb.save : |{}|'.format(err))
        return False
    return True

def fStr_FindArea_NextArray(xlWs, str_area):
    int_skipBelow = int(str_area.split('-')[1])
    str_areaStart = str_area.split('-')[2]
    # Loop on Skip Below integer
    str_areaEnd = str_areaStart
    for _ in range(int_skipBelow):
        str_areaEnd = fRg_FindCellDown(xlWs, str_areaEnd)
    return str_areaEnd

def fStr_defineStyle(xlWb, d_formatValue):
    """Define and add a Style format depending on a name dev created (NikkoHeader_Blue) """
    try:
        # ----------------------------------------------
        # Define the Style NAME
        #   {'font':{'name':'Calibri', 'size':9}}
        l_styleName = list(d_formatValue.keys())
        for dic in list(d_formatValue.values()):
            if isinstance(dic, dict):
                l_styleName.extend(list(dic.keys()))
                l_styleName.extend(list(dic.values()))
        str_styleName = '_'.join([str(x) for x in l_styleName])
        str_styleName = str_styleName.replace(' ', '')
        # ----------------------------------------------
        # Format Date
        if 'date' in d_formatValue:
            str_formatDate = d_formatValue['date']
            o_style = styl.NamedStyle(name=str_styleName, number_format=str_formatDate)
        else:
            o_style = styl.NamedStyle(name=str_styleName)

        # Conditional
        if 'font' in d_formatValue:
            d_font = d_formatValue['font']
            o_style.font = styl.Font(**d_font)
        if 'fill' in d_formatValue:
            d_fill = d_formatValue['fill']
            o_style.fill = styl.PatternFill(**d_fill)
        if 'alignment' in d_formatValue:
            d_align = d_formatValue['alignment']
            o_style.alignment = styl.Alignment(**d_align)
    except Exception as err:
        logger.error(' ERROR fStr_definStyle: Loop on Area for Style : |{}|'.format(err))
        logger.error('  - ** ARGS : |{}|'.format(str_styleName))
        logger.error(o_style)
        logger.error(d_formatValue)
        raise
    # Save the Style in WK
    try:
        xlWb.add_named_style(o_style)
    except:
        pass  # logger.warning('    (*) Information: Style already exists in the workbook: {}'.format(str_styleName))
    return str_styleName

def Act_loopFormat(l_rows, str_styleName, str_type=''):
    """ Loop Cell by Cell to apply a format """
    try:
        for row in l_rows:
            for cell in row:
                if 'num_format' in str_type.lower():
                    cell.number_format = str_styleName
                else:
                    cell.style = str_styleName
    except Exception as err:
        logger.error(' ERROR Act_loopFormat: Loop on Area for Style : |{}|'.format(err))
        logger.error('  - ** ARGS : |{}|'.format(str_styleName))
        try:
            logger.error(row)
            logger.error(cell)
        except:
            pass
        raise

def Act_resizeRowColumn(xlWs, str_type, d_formatValue):
    try:
        if 'col' in str_type:
            for col in d_formatValue:
                col_dimension = d_formatValue[col]
                if isinstance(col_dimension, int):
                    xlWs.column_dimensions[col].width = col_dimension
                else:
                    logger.error(' ERROR in Act_resizRowColumn - Column_size need to be an integer')
        elif 'row' in str_type:
            for row in d_formatValue:
                row_dimension = d_formatValue[row]
                if isinstance(row_dimension, int):
                    xlWs.row_dimensions[row].height = row_dimension
                else:
                    logger.error(' ERROR in Act_resizRowColumn - row_dimension need to be an integer')
    except Exception as err:
        logger.error('  ERROR in Act_resizRowColumn : |{}|'.format(err))
        raise

def Act_loopBorder(str_type, rg_toSelect, str_borderName, bl_full=False, bl_row=False):
    try:
        if str_borderName == 'normBlack':
            o_border = styl.Side(border_style='thin')
        elif str_borderName == 'WT_blue':
            o_border = styl.Side(border_style='thin', color='4A7FB0')
        elif str_borderName == 'Green_Pale':
            o_border = styl.Side(border_style='thin', color='9BBB59')
        else:
            try:
                o_border = styl.Side(border_style='thin', color=str_borderName)
            except:
                o_border = styl.Side(border_style='thin')
                logger.warning('\n  **Please define a correct Border in Act_lopBorder || {}'.format(str_borderName))
                logger.warning('      Will use Black for now')

        # ===========================
        # Full Array => *Ignore all below condition
        if bl_full is True:
            for row in rg_toSelect:
                for cell in row:
                    cell.border = styl.Border(top=o_border, bottom=o_border, left=o_border, right=o_border)
            return True
        elif bl_row is True:
            for row in rg_toSelect:
                for cell in row:
                    cell.border = styl.Border(top=o_border, bottom=o_border)
            return True

        # ===========================
        # Get the characteristics of the Array
        if rg_toSelect[0] == rg_toSelect[-1]:
            bl_uniqueRow = True
            if rg_toSelect[0][0] == rg_toSelect[0][-1]:
                bl_uniqueCell = True
            else:
                bl_uniqueCell = False
        else:
            bl_uniqueCell = False
            bl_uniqueRow = False
            if rg_toSelect[0][0] == rg_toSelect[0][-1]:
                bl_uniqueCol = True
            else:
                bl_uniqueCol = False
        # ===========================
        # I. One Cell
        if bl_uniqueCell:
            cell = rg_toSelect[0][0]
            cell.border = styl.Border(top=o_border, bottom=o_border, left=o_border, right=o_border)
            return True
        # ===========================
        # II. One Row
        if bl_uniqueRow:
            row_unique = rg_toSelect[0]
            for cell in row_unique:
                # left cell
                if cell == row_unique[0]:
                    cell.border = styl.Border(top=o_border, bottom=o_border, left=o_border)
                # right cell
                elif cell == row_unique[-1]:
                    cell.border = styl.Border(top=o_border, bottom=o_border, right=o_border)
                else:
                    cell.border = styl.Border(top=o_border, bottom=o_border)
            return True
        # ===========================
        # II. One column
        if bl_uniqueCol:
            for row in rg_toSelect:
                cell = row[0]
                # Top cell
                if cell == rg_toSelect[0][0]:
                    cell.border = styl.Border(left=o_border, right=o_border, top=o_border)
                # bottom cell
                elif cell == rg_toSelect[-1][0]:
                    cell.border = styl.Border(left=o_border, right=o_border, bottom=o_border)
                else:
                    cell.border = styl.Border(left=o_border, right=o_border)
            return True
        # ===========================
        # III. Proper Array
        # III.a. Loop for Left and right
        for row in rg_toSelect:
            cell_left = row[0]
            cell_right = row[-1]
            cell_left.border = styl.Border(left=o_border)
            cell_right.border = styl.Border(right=o_border)
        # III.b. Loop for Top
        row_top = rg_toSelect[0]
        for cell in row_top:
            # Top-left cell
            if cell == rg_toSelect[0][0]:
                cell.border = styl.Border(top=o_border, left=o_border)
            # Top-right cell
            elif cell == rg_toSelect[0][-1]:
                cell.border = styl.Border(top=o_border, right=o_border)
            else:
                cell.border = styl.Border(top=o_border)
        # III.c. Loop for bottom
        row_bottom = rg_toSelect[-1]
        for cell in row_bottom:
            # bottom-left cell
            if cell == rg_toSelect[-1][0]:
                cell.border = styl.Border(bottom=o_border, left=o_border)
            # bottom-right cell
            elif cell == rg_toSelect[-1][-1]:
                cell.border = styl.Border(bottom=o_border, right=o_border)
            else:
                cell.border = styl.Border(bottom=o_border)
    except Exception as err:
        logger.error('  ERROR in Act_lopBorder : |{}|'.format(err))
        logger.error('  - ** ARGS : |{}|-|{}|'.format(str_type, str_borderName))
        logger.error(rg_toSelect)
        logger.error(row)
        logger.error(cell)
        raise

def fDic_colNumber():
    d_cell = {0: 'A', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I',
              10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S',
              20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z', 27: 'AA', 28: 'AB', 29: 'AC',
              30: 'AD', 31: 'AE', 32: 'AF', 33: 'AG', 34: 'AH', 35: 'AI', 36: 'AJ', 37: 'AK', 38: 'AL', 39: 'AM',
              40: 'AN', 41: 'AO', 42: 'AP', 43: 'AQ', 44: 'AR', 45: 'AS', 46: 'AT', 47: 'AU', 48: 'AV', 49: 'AW',
              50: 'AX'}
    return d_cell

def fInt_findColumnNumber(str_colStart):
    # find The column number
    d_colNumber = fDic_colNumber()
    d_NumberCol = {value: key for key, value in d_colNumber.items() if key > 0}
    int_colBase = d_NumberCol[str_colStart]
    return int_colBase

def fStrInt_GetColAndRow(str_cell):
    # Get if  CELL is one letter or two
    try:
        str_secondChar = str_cell[1]
        if isinstance(int(str_secondChar), int):
            str_colStart = str_cell[0]
            int_rowHeader = int(str_cell[1:])
        else:
            raise
    except:
        str_colStart = str_cell[0:2]
        int_rowHeader = int(str_cell[2:])
    return str_colStart, int_rowHeader

def fInt_GetTheLastRowArray(xlWs, int_rowStart, int_colBase):
    i_rowNumFin = int_rowStart
    for i_numRow in range(1, 1_000_000):
        ROW = xlWs[int_rowStart + i_numRow]
        if (ROW[int_colBase].value == '') | (ROW[int_colBase].value == None):
            break
        i_rowNumFin += 1
    return i_rowNumFin

def fInt_GetTheFirstRowNextArray(xlWs, int_rowStart, int_colBase):
    i_rowNumNextArray = int_rowStart + 1
    for i_numRow in range(1, 1_000_000):
        ROW = xlWs[int_rowStart + i_numRow]
        if (ROW[int_colBase].value == '') | (ROW[int_colBase].value == None):
            i_rowNumNextArray += 1
        else:
            break
    return i_rowNumNextArray

def fRg_FindCellDown(xlWs, str_area):
    try:
        # Get if its a area of a cell
        if ':' in str_area:
            str_cellStart = str_area.split(':')[0]
        else:
            str_cellStart = str_area
        # Get the Address of the Cell
        str_colStart, int_rowHeader = fStrInt_GetColAndRow(str_cellStart)
        # find The column number
        int_colBase = fInt_findColumnNumber(str_colStart)
        # Find the end of the Array
        i_rowNumFin = fInt_GetTheLastRowArray(xlWs, int_rowHeader, int_colBase - 1)
        # Find the next Array
        i_rowNumNextArray = fInt_GetTheFirstRowNextArray(xlWs, i_rowNumFin, int_colBase - 1)
        # END
        if ':' in str_area:
            # Ecart de ligne
            int_diff = i_rowNumNextArray - int_rowHeader
            # get the Address of the seond cell
            str_cell = str_area.split(':')[1]
            str_col, int_row = fStrInt_GetColAndRow(str_cell)
            str_areaEnd = "{}{}:{}{}".format(str_colStart, i_rowNumNextArray, str_col, int_row + int_diff)
        else:
            str_areaEnd = "{}{}".format(str_colStart, i_rowNumNextArray)
    except Exception as err:
        logger.error(' ERROR fl fRg_FindCellDwn : |{}|'.format(err))
        logger.error('  - ** AREA : |{}|'.format(str_area))
        logger.error('  - int_colBase : |{}|'.format(str_cellStart))
        logger.error('  - int_colBase : |{}|'.format(int_colBase))
        logger.error('  - i_rowNumFin : |{}|'.format(i_rowNumFin))
        logger.error('  - i_rowNumNextArray : |{}|'.format(i_rowNumNextArray))
        raise
    return str_areaEnd

def fRg_SelectRangeToApplyFormat(xlWs, str_cell, bl_includeHeader=True, bl_column=False):
    try:
        # Get the Address of the Cell
        str_colStart, int_rowHeader = fStrInt_GetColAndRow(str_cell)
        # find The column number
        int_colBase = fInt_findColumnNumber(str_colStart)
        # Dic of Column letter <=> number
        d_colNumber = fDic_colNumber()

        # Find the end of the Array
        i_rowNumFin = fInt_GetTheLastRowArray(xlWs, int_rowHeader, int_colBase - 1)

        # Find the Row object
        row_header = xlWs[int_rowHeader]
        # include Header or not
        if not bl_includeHeader:    int_rowHeader += 1

        # Just on the column
        if bl_column:
            str_area = "{}{}:{}{}".format(str_colStart, int_rowHeader, str_colStart, i_rowNumFin)
        else:
            # ---------------------
            # Get the Max column
            i_colIter = 0
            i_colNumFin = int_colBase - 1
            for cell in row_header:
                if i_colIter < i_colNumFin:
                    # If we start at column B we dont want to take column A into account
                    i_colIter += 1
                else:
                    if cell.value == '' or cell.value == None:  break
                    i_colNumFin += 1
                    i_colIter += 1
            # Final
            str_area = "{}{}:{}{}".format(str_colStart, int_rowHeader, d_colNumber[i_colNumFin], i_rowNumFin)
        # ---------------------
        # Define Range
        rg_toSelect = xlWs[str_area]
        # ---------------------
    except Exception as err:
        logger.error(' ERROR fl fRg_SelectRgeToApplyFormat : |{}|'.format(err))
        logger.error('  - ** ARGS : |{}|-|{}|'.format(str_cell, str_area))
        logger.error(bl_includeHeader)
        logger.error(i_colNumFin)
        logger.error(i_rowNumFin)
        raise
    return rg_toSelect

def Act_reshapePrintFormat(xlWs, d_formatValue):
    try:
        for kle in d_formatValue:
            if kle == 'print_area':
                rangeToPrint = d_formatValue[kle]
                xlWs.print_area = rangeToPrint
            elif kle == 'print_fit':
                if d_formatValue[kle].lower() == 'true':
                    xlWs.page_setup.fitToPage = True
                    # xlWs.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage = True) #, autoPageBreaks = False
                    # xlWs.sheet_properties.pageSetUpPr.autoPageBreaks = True
                elif d_formatValue[kle].lower() == 'fittowidth':
                    xlWs.page_setup.fitToPage = True
                    xlWs.page_setup.fitToHeight = False
                elif d_formatValue[kle].lower() == 'fittoheight':
                    xlWs.page_setup.fitToPage = True
                    xlWs.page_setup.fitToWidth = False
    except Exception as err:
        logger.error('  ERROR in Act_reshapPrintFormat : |{}|'.format(err))
        raise
