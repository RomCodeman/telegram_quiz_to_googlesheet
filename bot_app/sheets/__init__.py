# bot_app.sheets.__init__.py
from bot_app.sheets.sheets_class import Sheet, subclasses_name_list
from bot_app.logger import logger

from typing import List

import gspread

logger.info("Initializing Google sheets and comparing sheets with classes in sheets_class.py ")

NUM = 31


# def column_positions(letter):
#     return ord(f"{letter}") & NUM


def num_to_letter(num: int):
    return chr(ord('@') + num)


try:
    worksheet_instances_list: List[gspread.models.Worksheet] = [worksheet for worksheet in Sheet.spreadsheet.worksheets()]
    worksheet_titles_list = sorted([worksheet.title for worksheet in worksheet_instances_list])
    subclasses_names_list = sorted([cls.__name__ for cls in Sheet.__subclasses__()])
    subclasses_list = Sheet.__subclasses__()
except Exception as e:
    raise e


# Sheet check
if worksheet_titles_list != subclasses_names_list:
    logger.warning(f"Sheets classes and {Sheet.book_name} sheet titles list are differ.")

    # Check for sheet's able in Google Sheets, but not used in the backend
    for worksheet in worksheet_instances_list:
        if worksheet.title not in subclasses_names_list:
            logger.warning(f"Unprocessable sheet {worksheet.title} was found in the book {Sheet.book_name}. "
                           f"Backend connection is needed.")

    # Check for sheet's classes, able in the backend, but not used in Google Sheets
    for subclass in subclasses_list:

        # Sheet not found. Create it and fill column titles
        if subclass.__name__ not in worksheet_titles_list:
            subclass.add_new_quiz_sheet()
            logger.info(f"Sheet '{subclass.__name__}' created")

            subclass.worksheet = subclass.worksheet_obtain()
            subclass.table_template_setup()
            logger.info(f"Column titles added: '{subclass.worksheet.row_values(1)}'")

        subclass: Sheet
        subclass.worksheet = subclass.worksheet_obtain()
        subclass_worksheet_title = subclass.worksheet.title
        sheet_part = subclass.worksheet.get(f"A1:{num_to_letter(len(subclass.column_titles_template))}10")

        # Not empty sheet found. Just warning
        if sheet_part:
            if sheet_part[0] != subclass.column_titles_template:
                logger.warning(f"{subclass_worksheet_title} was not empty. Manual handling needed.")
        # Empty sheet found. Insert c column titles template of subclass
        else:
            subclass.table_template_setup()
