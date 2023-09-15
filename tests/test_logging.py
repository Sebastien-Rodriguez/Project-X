"""_summary_
"""

import unittest
from project_x.tools.logging import Logging, LoggingLevel, LoggingSource


class TestLogging(unittest.TestCase):
    """Class bringing together 
    all the logging system tests.
    """

    def test_sigleton(self) -> None:
        """Test if the class 
        returns the same instance.
        """

        logging0 = Logging()
        logging1 = Logging()
        self.assertIs(logging0, logging1)


    async def test_start(self) -> None:
        """_summary_
        """
        logging = Logging()
        await logging.start()


    # async def test_stop(self) -> None:
    #     """_summary_
    #     """


    # async def test_create_file(self) -> None:
    #     """_summary_
    #     """

    # async def test_force_rotate_file(self) -> None:
    #     """_summary_
    #     """

    # async def test_auto_rotate_file(self) -> None:
    #     """_summary_
    #     """

    # def test_format_log(self) -> None:
    #     """_summary_
    #     """

    # async def add_log(self) -> None:
    #     """_summary_
    #     """

    # async def test_level_logging(self) -> None:
    #     """_summary_
    #     """

    # async def test_source_logging(self) -> None:
    #     """_summary_
    #     """
