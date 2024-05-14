from enum import Enum
import logging
import sys


from corelib.utils.configuration_builder import Settings


class LoggerType(Enum):
    """
    This Enum has the list of all the available loggers
    """
    FILE_LOGGER = 'FILE'


class LoggerFactory(object):

    FILE_LOG = None

    @staticmethod
    def __create_file_logger(log_file,  log_level):
        """
        A method for configuring logger that write logs to specified log file. 
        The logging configuration are provided using settings file
        """
        # set the logging format
        log_format = "%(asctime)s:%(levelname)s:%(message)s"
        

        logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        LoggerFactory.FILE_LOG = logging.getLogger('ragQuery_Logger',)
        
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)

        # set the logging level based on configuration
        if log_level == "INFO":         
            fh.setLevel(logging.INFO)
        elif log_level == "ERROR":
            fh.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            fh.setLevel(logging.DEBUG)

        LoggerFactory.FILE_LOG.addHandler(fh)

        return LoggerFactory.FILE_LOG

    @staticmethod
    def get_logger(settings:Settings)->logging.Logger:
        """
        Method for getting logger
        """
        if settings.logger_type == LoggerType.FILE_LOGGER.value:
            # Don't re-initialize existing kind of logger in the system
            if LoggerFactory.FILE_LOG != None:
                return LoggerFactory.FILE_LOG  
            logger = LoggerFactory.__create_file_logger(settings.log_file, settings.log_level)
        else:
            raise Exception(f'Incorrect logger type {settings.logger_type} provided')
        
        return logger