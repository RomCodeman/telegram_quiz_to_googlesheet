import gspread

from bot_app.logger import logger
from config import client_gspread


# Auxiliary class (temporary solution)
class UserCredentials:
    def __init__(self, chat_id):
        self.chat_id: int = chat_id
        self.login: str = ""
        self.name: str = ""
        self.phone_num: str = ""
        self.answers: list = []

    def __str__(self):
        return f"chat_id: {self.chat_id}, login: {self.login}, name: {self.name}, phone_num: {self.phone_num}, answers: {self.answers}"


# quiz_tables Book. Each subclass is a single quiz.
class Sheet:
    book_name = "quiz_tables"
    column_titles_template: list = []
    spreadsheet: gspread.models.Spreadsheet = client_gspread.open(book_name)
    worksheet: gspread.models.Worksheet = None

    def __init__(self, user: UserCredentials):
        self._worksheet_title = self.__class__.__name__
        self.column_titles_template = self.__class__.column_titles_set()
        self.chat_id = user.chat_id
        self.u_login = user.login
        self.u_name = user.name
        self.u_phone_num = user.phone_num
        self.u_answer = user.answers

    @classmethod
    def add_new_quiz_sheet(cls):
        cls.spreadsheet.add_worksheet(title=cls.__name__, rows=100, cols=len(cls.column_titles_template))

    @classmethod
    def worksheet_obtain(cls):
        try:
            worksheet: gspread.models.Worksheet = cls.spreadsheet.worksheet(title=cls.__name__)
            return worksheet
        except Exception as e:
            logger.error(f"Unable to get a worksheet for a {cls.__name__} class. Exception: {e}")

    @classmethod
    def column_titles_set(cls):
        return cls.column_titles_template

    def save_to_sheet(self):
        self.worksheet.append_row([f"{self.chat_id}", f"{self.u_login}", f"{self.u_name}", f"{self.u_phone_num}",
                                   f"{', '.join(self.u_answer)}"])

    @classmethod
    def table_template_setup(cls):
        cls.worksheet.insert_row(cls.column_titles_template, 1)
        logger.warning(f"Column titles corrected in accordance with '{cls.__name__}.column_titles_template'.")


sheet_list = Sheet.__subclasses__()
subclasses_name_list = [cls.__name__ for cls in Sheet.__subclasses__()]


class QuestionnaireSheet(Sheet):
    column_titles_template = ['chat_id', 'u_login', 'u_name', 'u_phone_num', 'u_answer']

    def __init__(self, user):
        super().__init__(user)


# Temporary class for sheet automatic creation testing
class TempSheet(Sheet):
    column_titles_template = ['temp1', 'temp2', 'temp3', 'temp4', 'temp5']

    def __init__(self, user):
        super().__init__(user)
