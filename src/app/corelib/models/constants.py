from enum import Enum


class Statuses(Enum):
    """
    Enum constant for different stages of processing
    """
    NotStarted = 1
    InProcess = 2
    Success = 3
    Failure = 4


class FileTypes(Enum):
    """
    Enum for different supported file types
    """

    PDF = 'pdf'
    TIFF = 'tiff'
    PNG = 'png'
    JPEG = 'jpeg'
    JPG = 'jpg'