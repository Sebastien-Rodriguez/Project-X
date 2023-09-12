from .logging import *


# il faut rectifié on a un circlar import
from configparser import ConfigParser
config_logging = ConfigParser()
config_logging.read("project_x/config/logging.ini")
