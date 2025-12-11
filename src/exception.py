"""
Provides more context (File & Line) than the standard Python Exception
"""
import sys 

def error_message_detail(error, error_detail:sys):

    # We only need the traceback (exc_tb) to find the line number
    _,_,exc_tb=error_detail.exc_info()

    # If there is no traceback, return the basic error
    if exc_tb is None:
        return str(error)
    
    # Get the filename from the stack frame
    file_name=exc_tb.tb_frame.f_code.co_filename

    # Format the detailed error message
    error_message="Error occured in Python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message