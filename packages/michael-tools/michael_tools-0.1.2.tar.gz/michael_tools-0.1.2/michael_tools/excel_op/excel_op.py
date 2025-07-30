# 处理查询结果，转换为DataFrame
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


def format_pd_datetime_columns(db_res):
    if not db_res:
        return None

    df = pd.DataFrame(db_res)

    # 处理日期时间列
    for col in df.columns:
        # A if B else C：如果 B 是 True，就返回 A，否则返回 C
        if isinstance(df[col].iloc[0], datetime) if not df.empty else False:
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df


def initialize_workbook():
    workbook = Workbook()
    # 删除默认创建的工作表
    if "Sheet" in workbook.sheetnames:
        workbook.remove(workbook.active)

    return workbook


# 调整 Excel 工作表的列宽
def adjust_column_width(worksheet, df, width_multiplier):
    for i, col in enumerate(df.columns):
        column_width = max(df[col].astype(str).map(len).max(), len(col)) * width_multiplier
        worksheet.column_dimensions[get_column_letter(i + 1)].width = column_width


# 创建新的 Excel工作表，并写入数据
def create_sheet_to_excel(workbook, sheet_name, df, width_multiplier=1.7):
    # 如果工作表已存在，删除它
    if sheet_name in workbook.sheetnames:
        idx = workbook.sheetnames.index(sheet_name)
        workbook.remove(workbook.worksheets[idx])

    # 创建新工作表
    worksheet = workbook.create_sheet(sheet_name)

    # 写入标题行
    for i, col in enumerate(df.columns):
        worksheet.cell(row=1, column=i + 1, value=col)

    # 写入数据行
    for r_idx, row in enumerate(df.values):
        for c_idx, value in enumerate(row):
            worksheet.cell(row=r_idx + 2, column=c_idx + 1, value=value)

    # 调整列宽
    adjust_column_width(worksheet, df, width_multiplier)

    return worksheet
