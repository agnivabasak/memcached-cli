import sys
import os
import click

sys.path.append(os.path.join(os.getcwd(),'..'))

import unittest
from unittest.mock import create_autospec
from memclid.constants import STATUS_RECORD_NOT_STORED, STATUS_RECORD_STORED
from memclid.svc_memclid import MemclidUtility
from memclid.memclid_socket import MemclidSocket

class TestDecrMemclidUtility(unittest.TestCase):
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
    
    def test_decr_store_success(self):
        
        """
            TEST 1 : Check if correct decr request is being made and
            decrementing the value corresponding to the key using decr 
            successfully leads to a success result in the application
        """
        self.memclidSocket.receive.return_value = "10\r\n"
        expectedResult = {
            "updated_value": "10",
            "message": "The value for the key was decremented successfully",
            "status": STATUS_RECORD_STORED
        }

        actualResult=self.memclidUtility.decr("testKey",5)
        self.memclidSocket.send.assert_called_once_with(msg="decr testKey 5\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_decr_store_failure(self):
        
        """
            TEST 2 : Check if correct decr request is being made and
            failure while decrementing the value corresponding to the key
            using decr leads to a failure result in the application
        """
        self.memclidSocket.receive.return_value = "NOT_FOUND\r\n"
        expectedResult = {
            "updated_value": None,
            "message": "The key doesnt exist in the memcached server. It could not be decremented due to the preconditions of the command executed.",
            "status": STATUS_RECORD_NOT_STORED
        }

        actualResult=self.memclidUtility.decr("testKey",5)
        self.memclidSocket.send.assert_called_once_with(msg="decr testKey 5\r\n")
        self.memclidSocket.receive.assert_called_once();
        self.assertDictEqual(actualResult,expectedResult)

    def test_decr_invalid_response(self):

        """
            TEST 3 : Check if MemclidUnrecognizedResponseSentByServer is raised and handled when an invalid response is sent by the server

        """
        self.memclidSocket.receive.return_value = "RANDOM_RESPONSE_SENT_BY_SERVER\r\n"

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.decr("testKey",5)

    def test_decr_handle_random_exception(self):

        """
            TEST 4 : Check if any random exception thrown is handled properly

        """

        self.memclidSocket.send.side_effect = Exception("Random Exception")

        with self.assertRaises(click.exceptions.Abort):
            self.memclidUtility.decr("testKey",5)
    
if __name__ == '__main__':
    unittest.main()
