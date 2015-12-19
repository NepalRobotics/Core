""" Tests for the custom logging system. """


import logging
import unittest

from messaging import Messenger
import nr_logger


class TestQueueLogging(unittest.TestCase):
  """ Tests for the QueueLoggingHandler and QueueLogger classes. (It's sort of
  hard to test them individually.) """

  def setUp(self):
    # Initialize the system with the logging queue.
    self.messenger = Messenger()
    nr_logger.QueueLogger.set_queue(self.messenger.get_queue("logging"))

    # Make a logger.
    self.logger = logging.getLogger("test")

  def test_message_transfer(self):
    """ Try logging a basic message and make sure it ends up on the queue. """
    message = "Help, I'm trapped in a robot factory!"

    self.logger.debug(message)

    # Read it from the queue.
    queue = self.messenger.get_queue("logging")
    new_message = queue.get()
    self.assertTrue(queue.empty())
    self.assertIn(message, new_message)
