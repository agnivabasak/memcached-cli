import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_RECORD_NOT_DELETED, STATUS_RECORD_DELETED
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestDeleteMemclidUtility(unittest.TestCase):
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
    
    def test_delete_success(self):
        
        """
            TEST 1 : Check if correct delete request is being made and
            deleting the key-value pair using delete successfully leads to a success result in the application
        """
        self.memclidSocket.receive.return_value = "DELETED\r\n"
        expectedResult = {
            "message": "The data was deleted successfully",
            "status": STATUS_RECORD_DELETED
        }

        actualResult=self.memclidUtility.delete("testKey")
        self.memclidSocket.send.assert_called_once_with(msg="delete testKey\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_delete_failure(self):
        
        """
            TEST 2 : Check if correct delete request is being made and
            failure while deleting the key-value pair using delete leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "NOT_FOUND\r\n"
        expectedResult = {
            "message": "The record was not found in the memcached server. It could not be deleted due to the preconditions of the command executed.",
            "status": STATUS_RECORD_NOT_DELETED
        }

        actualResult=self.memclidUtility.delete("testKey")
        self.memclidSocket.send.assert_called_once_with(msg="delete testKey\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_delete_invalid_response(self):

        """
            TEST 3 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "RANDOM_RESPONSE_SENT_BY_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.delete("testKey")

    def test_add_handle_random_exception(self):

        """
            TEST 4 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.delete("testKey")
    
if __name__ == '__main__':
    unittest.main()
