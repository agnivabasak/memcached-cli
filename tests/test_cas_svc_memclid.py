import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_RECORD_NOT_STORED, STATUS_RECORD_STORED
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestCasMemclidUtility(unittest.TestCase):
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

    def test_cas_store_success(self):
        
        """
            TEST 1 : Check if correct cas request is being made and
            replacing the value for an already exisitng and not modified key successfully leads to a success result in the application
        """
        self.memclidSocket.receive.return_value = "STORED\r\n"
        expectedResult = {
            "message": "The value for the key was set successfully",
            "status": STATUS_RECORD_STORED
        }

        actualResult=self.memclidUtility.cas("testKey","testValueNew",8,1000,3600)
        self.memclidSocket.send.assert_called_once_with(msg="cas testKey 1000 3600 12 8\r\ntestValueNew\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_cas_store_failure_because_modified(self):
        
        """
            TEST 2 : Check if correct cas request is being made and
            failure while storing the key-value pair using cas as someone has modified it
            since it was last fetched
            leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "EXISTS\r\n"
        expectedResult = {
            "message": "The value was modified since it was last fetched. It could not be stored due to the preconditions of the command executed.",
            "status": STATUS_RECORD_NOT_STORED
        }

        actualResult=self.memclidUtility.cas("testKey","testValueNew",8,1000,3600)
        self.memclidSocket.send.assert_called_once_with(msg="cas testKey 1000 3600 12 8\r\ntestValueNew\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_cas_store_failure_because_not_found(self):
        
        """
            TEST 3 : Check if correct cas request is being made and
            failure while storing the key-value pair using cas as someone has modified it
            since it was last fetched
            leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "NOT_FOUND\r\n"
        expectedResult = {
            "message": "The key doesnt exist in the memcached server. It could not be stored due to the preconditions of the command executed.",
            "status": STATUS_RECORD_NOT_STORED
        }

        actualResult=self.memclidUtility.cas("testKey","testValueNew",8,1000,3600)
        self.memclidSocket.send.assert_called_once_with(msg="cas testKey 1000 3600 12 8\r\ntestValueNew\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_cas_invalid_response(self):

        """
            TEST 4 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "UNKNOWN_RESPONSE_SENT_BY_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.cas("testKey","testValueNew",8,1000,3600)

    def test_cas_handle_random_exception(self):

        """
            TEST 4 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.cas("testKey","testValueNew",8,1000,3600)
    

if __name__ == '__main__':
    unittest.main()
