import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_DATA_AVAILABLE, STATUS_DATA_NOT_AVAILABLE
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestGetMemclidUtility(unittest.TestCase):
    """
    Essentially these unit tests test that the application can interpret the messages sent by
    the Memcached server (through socket connection) and that it handles it correctly
    """
    def setUp(self):
        self.memclidSocket = create_autospec(MemclidSocket)
        self.memclidSocket.host = "localhost"
        self.memclidSocket.port = 11211
        self.memclidUtility = MemclidUtility(self.memclidSocket)
    
    def tearDown(self):
        self.memclidUtility = None
        self.memclidSocket = None
    
    def test_get_correct_value(self):
        
        """
            TEST 1 : Check if correct get request is being made and 
            correct value is fetched (given it exists in the memcached server)
        """
        self.memclidSocket.receive.return_value = "VALUE testKey 10 9\r\ntestValue\r\nEND\r\n"
        expectedResult = {
            "flag": "10",
            "value": "testValue",
            "message": "Fetched the value for testKey",
            "status": STATUS_DATA_AVAILABLE
        }

        actualResult=self.memclidUtility.get("testKey")
        self.memclidSocket.send.assert_called_once_with(msg="get testKey\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_get_no_value(self):

        """
            TEST 2 : Check if correct get request is being made  and
            key not being present in the memcached server is handled properly
        """
        self.memclidSocket.receive.return_value = "END\r\n"
        expectedResult = {
            "flag": None,
            "value": None,
            "message": "No value found for testKey",
            "status": STATUS_DATA_NOT_AVAILABLE
        }

        actualResult=self.memclidUtility.get("testKey")
        self.memclidSocket.send.assert_called_once_with(msg="get testKey\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)
    
    def test_get_invalid_response(self):

        """
            TEST 3 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "INVALID_RESPONSE_FROM_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.get("testKey")

    def test_get_handle_random_exception(self):

        """
            TEST 4 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.get("testKey")


if __name__ == '__main__':
    unittest.main()
