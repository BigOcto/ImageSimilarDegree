import os
import xlsxwriter
from xlrd import open_workbook
from xlutils.copy import copy


def write_excel(data_list, file_name, version):
    if os.path.exists(file_name):
        update_excel(file_name, str(version), data_list)
    else:
        create_excel(file_name)
        update_excel(file_name, str(version), data_list)


def create_excel(excel_file):
    workbook = xlsxwriter.Workbook(excel_file)
    workbook.close()


def read_excel_data_by_col(version, sheet_num, file_name):
    if os.path.exists(file_name):
        work_book = open_workbook(file_name)
        work_sheet = work_book.sheet_by_index(sheet_num)
        row_data_list = []
        try:
            col_num = read_excel_version_col(version, work_sheet)
            row_data_list = work_sheet.col_values(col_num)
        except Exception as e:
            print(str(e))
        return row_data_list
    else:
        print('File not exist !!')
        exit()


def update_excel(excel_file, version, data_list):
    work_book = open_workbook(excel_file)
    work_sheet = work_book.sheet_by_index(0)
    excel = copy(work_book)
    table_sheet = excel.get_sheet(0)
    match_exist_col = read_excel_version_col(version, work_sheet)

    if match_exist_col != -1:
        real_row_length = read_row_size(work_sheet, match_exist_col)
        print("match col : ", match_exist_col, "real row length ", real_row_length)
        for i, data in enumerate(data_list):
            table_sheet.write(real_row_length + i, match_exist_col, data)
    else:
        cul_count = work_sheet.ncols
        table_sheet.write(0, cul_count, version)
        for i, statN in enumerate(data_list):
            table_sheet.write(i + 1, cul_count, statN)
    print('Write ' + excel_file + " size: ", len(data_list), ' success!')
    excel.save(excel_file)


def read_excel_version_col(version, worksheet):
    first_row_list = []
    try:
        first_row_list = worksheet.row_values(0)
    except Exception as e:
        print(str(e))
    col = -1
    for c in first_row_list:
        col += 1
        if version == c:
            print(version + " col exist, break,", "col number :", col)
            return col

    print(version + " col not exist, write normal")
    return -1


# get one column's real length
def read_row_size(worksheet, col):
    row_data_list = []
    try:
        row_data_list = worksheet.col_values(col)
    except Exception as e:
        print(str(e))
    row_length = len(row_data_list)
    for col in range(row_length - 1, 0, -1):
        if str(row_data_list[col]) == "" or str(row_data_list[col]) == '':
            row_length -= 1
        else:
            break
    print("cul real size : " + str(row_length))
    return row_length
