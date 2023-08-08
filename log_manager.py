import logging
from logging.handlers import RotatingFileHandler
import sys
from uio import StringIO


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler_file = RotatingFileHandler("temp_sensor.log", maxBytes= 100 * 1000, backupCount=2) # Onboard flash = 2MB.
handler_file.setFormatter(formatter)
logging.getLogger().addHandler(handler_file)

root = logging.getLogger()


def get_logger(name):
    logger = logging.getLogger(name)
    logger.handlers = root.handlers
    return logger


def get_stack_trace(e):
    stack_trace = StringIO()
    sys.print_exception(e, stack_trace)
    stack_trace = stack_trace.getvalue()
    return stack_trace
