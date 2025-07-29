import logging
import http.client
import traceback


class SingletonLoggerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonLoggerMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    white = "\x1b[1;97m"
    green = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    purple = "\x1b[1;95m"
    reset = "\x1b[0m"

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.FORMATS = {
            logging.DEBUG: CustomFormatter.grey + fmt + CustomFormatter.reset,
            logging.INFO: CustomFormatter.white + fmt + CustomFormatter.reset,
            logging.WARNING: CustomFormatter.yellow + fmt + CustomFormatter.reset,
            logging.WARN: CustomFormatter.purple + fmt + CustomFormatter.reset,
            logging.ERROR: CustomFormatter.red + fmt + CustomFormatter.reset,
            logging.CRITICAL: CustomFormatter.bold_red + fmt + CustomFormatter.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomLogging(metaclass=SingletonLoggerMeta):
    # *********************** Internal methods *********************** #
    def __init__(self, enable_wire_logging: bool = False):
        super().__init__()
        self.enable_wire_logging = enable_wire_logging
        CRITICAL = 50
        FATAL = CRITICAL
        E_ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
        self._log_levels = {
            'CRITICAL': CRITICAL,
            'FATAL': FATAL,
            'ERROR': E_ERROR,
            'WARN': WARNING,
            'WARNING': WARNING,
            'INFO': INFO,
            'DEBUG': DEBUG,
            'NOTSET': NOTSET,
        }

    # *********************** External methods *********************** #
    def getLogger(self, logger_name, create_file=False) -> logging.Logger:
        try:
            console_log_level: int = self._log_levels["INFO"]
            file_log_level: int = self._log_levels["INFO"]

            log: logging.Logger = logging.getLogger(logger_name)

            log.setLevel(level=console_log_level)
            formatter = CustomFormatter("%(asctime)s - [ %(filename)s : %(lineno)s ]: %(message)s", "%H:%M:%S - %d/%m/%Y")
            if create_file:
                fh = logging.FileHandler("./application.log")
                fh.setLevel(level=file_log_level)
                fh.setFormatter(formatter)
                log.addHandler(fh)

            # create console handler for logger.
            ch = logging.StreamHandler()
            ch.setLevel(level=console_log_level)
            ch.setFormatter(formatter)
            log.addHandler(ch)

            if self.enable_wire_logging:
                http.client.HTTPConnection.debuglevel = 1

            return log
        except Exception as exp:
            traceback.print_exc()
            print(f"ERROR: {exp}: Something went wrong")
            raise exp
