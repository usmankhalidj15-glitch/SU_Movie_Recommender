import sys, os
from src.logging.logger import logging
class CustomException(Exception):
    def __init__(self, error_message, error_detail : sys):
        self.error_message = error_message
        _, _, exc_tb = error_detail.exc_info()

        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"error occured in python script [{self.file_name}] line number [{self.line_number}] error message [{self.error_message}]"
    
