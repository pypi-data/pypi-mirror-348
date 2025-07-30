import logging
from enum import Enum
from threading import Lock


class LogColors(Enum):
    """
    Enum to define various ANSI color codes for colored log output.
    """
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    NONE = None


class ColoredFormatter(logging.Formatter):
    """
    Custom log formatter that applies color to the log message.

    :param color: LogColors Enum, defines the color to be applied to the log message.
    :param custom_format: Optional log message format string.

    """

    def __init__(self, color: LogColors, custom_format=None):
        super().__init__(custom_format)
        self.color = color

    def format(self, record):
        """
        Formats the log message by applying the selected color to the log message.

        :param record: The log record to be formatted.
        :returns: The formatted log message string with ANSI color codes.
        """
        log_fmt = f"{self.color.value}%(asctime)s - %(name)s - %(lineno)d - %(threadName)s - %(levelname)s - %(message)s{LogColors.RESET.value}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class IBMLogger:
    """
    Logger class to be instantiated and used in the modules
    Logger class supports thread-safe instantiation and different color formatting for each logger instance.

    :param name: Name of the logger.
    :param log_level: The log level (e.g., 'DEBUG', 'INFO'), default is 'DEBUG'.
    :param log_file_path: File path to write logs, if specified.
    :param color: The color to be applied to the logs, from the :class:`LogColors` Enum.
    """
    _lock = Lock()

    def __init__(self, name, log_level="DEBUG", log_file_path="app.log", color: LogColors = LogColors.RESET):

        with IBMLogger._lock:
            self.log = logging.getLogger(name)
            if not self.log.handlers:
                self._initialize_logger(log_level, name, log_file_path, color)

    def _initialize_logger(self, log_level, name, log_file_path, color: LogColors):
        """
        Initialises logger basic configuration.
        Sets up the logger with a console handler and an optional file handler.
        Ensures that handlers are only added once.

        :param log_level: Log level (this is passed as argument to the main)
        :param log_file_path: Log file path where the log file should be created
        :param color: The color to be applied to the logs, from the :class:`LogColors` Enum.
        """
        self.log.setLevel(log_level.upper())

        if not self.log.handlers:
            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level.upper())
            console_handler.setFormatter(ColoredFormatter(color))

            # File Handler
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(log_level.upper())
            file_handler.setFormatter(self._get_formatter())

            # Adding handlers to the logger
            self.log.addHandler(console_handler)
            self.log.addHandler(file_handler)

    @staticmethod
    def _get_formatter():
        """
        Simple formatter without color coding. Used for file handlers.
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(lineno)d - %(threadName)s - %(levelname)s - %(message)s")

    def get_logger(self):
        """
        Fetch logger object
        :returns: logger object of :class:`logging.Logger`

        """
        return self.log
