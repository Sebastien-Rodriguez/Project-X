from enum import Enum
import os


class ConfigPath(Enum):
    """It's an Enum class containing all the config paths.

    ALLCONFIG member is a tuple of all config path.
    """

    GLOBAL = os.path.abspath("project_x/config/global.ini")
    API = os.path.abspath("project_x/config/api.ini")
    COMPRETEUR = os.path.abspath("project_x/config/compreteur.ini")
    DATABASE = os.path.abspath("project_x/config/database.ini")
    MODERATION = os.path.abspath("project_x/config/moderation.ini")
    PROMOTE = os.path.abspath("project_x/config/promote.ini")
    SUPPORT = os.path.abspath("project_x/config/support.ini")
    VOICE = os.path.abspath("project_x/config/voice.ini")

    ALLCONFIG: tuple = (GLOBAL, API, COMPRETEUR, 
                        DATABASE, MODERATION, PROMOTE,
                        SUPPORT, VOICE)
