import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_RECORD_NOT_STORED, STATUS_RECORD_STORED
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestAppendMemclidUtility(unittest.TestCase):
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

    def test_append_store_success(self):
        
        """
            TEST 1 : Check if correct append request is being made and
            appending the value for an already exisiting key successfully leads to a success result in the application
        """
        self.memclidSocket.receive.return_value = "STORED\r\n"
        expectedResult = {
            "message": "The value was appended successfully",
            "status": STATUS_RECORD_STORED
        }

        actualResult=self.memclidUtility.append("testKey","appendedValue")
        self.memclidSocket.send.assert_called_once_with(msg="append testKey 0 3600 13\r\nappendedValue\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_append_store_failure(self):
        
        """
            TEST 2 : Check if correct append request is being made and
            failure while storing the key-value pair using append leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "NOT_STORED\r\n"
        expectedResult = {
            "message": "The key most likely doesnt exist in the memcached server. It could not be stored.",
            "status": STATUS_RECORD_NOT_STORED
        }

        actualResult=self.memclidUtility.append("testKey","appendedValue")
        self.memclidSocket.send.assert_called_once_with(msg="append testKey 0 3600 13\r\nappendedValue\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_append_invalid_response(self):

        """
            TEST 3 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "UNKNOWN_RESPONSE_SENT_BY_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.append("testKey","appendedValue")

    def test_append_handle_random_exception(self):

        """
            TEST 4 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.append("testKey","appendedValue")
    

if __name__ == '__main__':
    unittest.main()
