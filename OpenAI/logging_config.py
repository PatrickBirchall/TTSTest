import logging
import sys

def configure_print_logging():

    class MessageOnlyFormatter(logging.Formatter):
        def format(self, record):
            return f"{str(record.name)}: {str(record.levelno)}: {str(record.msg)}"

    class PrintLogger(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            print(msg)
            sys.stdout.flush()

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = PrintLogger()
    handler.setFormatter(MessageOnlyFormatter())
    root_logger.addHandler(handler)

    for logger_name in ["uvicorn", "fastapi", "openai", "starlette", "__main__", "app"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
