import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_DATA_AVAILABLE, STATUS_DATA_NOT_AVAILABLE, STATUS_RECORD_NOT_STORED, STATUS_RECORD_STORED
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestMemclidUtility(unittest.TestCase):
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
            TEST 1 : Check if correct value is fetched (given it exists in the memcached server)
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
            TEST 2 : Check if key not being present in the memcached server is handled properly
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

    def test_set_store_success(self):
        
        """
            TEST 5 : Check if storing the key-value pair successfully leads to a success result in the application
        """
        self.memclidSocket.receive.return_value = "STORED\r\n"
        expectedResult = {
            "message": "The data was saved successfully",
            "status": STATUS_RECORD_STORED
        }

        actualResult=self.memclidUtility.set("testKey","testValue",10,60)
        self.memclidSocket.send.assert_called_once_with(msg="set testKey 10 60 9\r\ntestValue\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_set_store_failure(self):
        
        """
            TEST 6 : Check if failure while storing the key-value pair leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "NOT_STORED\r\n"
        expectedResult = {
            "message": "The data could not be stored",
            "status": STATUS_RECORD_NOT_STORED
        }

        actualResult=self.memclidUtility.set("testKey","testValue",10,60)
        self.memclidSocket.send.assert_called_once_with(msg="set testKey 10 60 9\r\ntestValue\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_set_invalid_response(self):

        """
            TEST 7 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "UNRECOGNIZED_RESPONSE_SENT_BY_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.set("testKey","testValue",0,3600)

    def test_set_handle_random_exception(self):

        """
            TEST 8 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.set("testKey","testValue",0,3600)

if __name__ == '__main__':
    unittest.main()
