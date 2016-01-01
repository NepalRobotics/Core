""" Tests for messaging.py. """


from multiprocessing import Process
import time
import unittest

import messaging


class TestMailbox(unittest.TestCase):
  """ Tests for the Mailbox class. """

  class TestingProcess(Process):
    """ A small class for testing in a multiprocessed environment. """

    def __init__(self, mailbox):
      """ Args:
        mailbox: The mailbox we will be using for testing. """
      super(TestMailbox.TestingProcess, self).__init__()

      self.__box = mailbox

    def run(self):
      """ Run the process. """
      # Wait until it is read.
      self.__box.wait_for_read()
      # Now set a new one.
      self.__box.set("meritocracy")

  def setUp(self):
    self.test_box = messaging.Messenger.Mailbox()

  def test_basic(self):
    """ A test of the basic functionality of Mailbox. """
    # It should start empty.
    self.assertEqual(None, self.test_box.get())

    # Set it and read back.
    self.test_box.set("test message")
    self.assertEqual("test message", self.test_box.get())

    # It should have nothing in it again.
    self.assertEqual(None, self.test_box.get())

  def test_overwrite(self):
    """ Tests that it behaves correctly when a value is already set. """
    self.test_box.set("The Honorable Dr. Shirley Ann Jackson")
    self.test_box.set("Shurlz")

    self.assertEqual(self.test_box.get(), "Shurlz")

  def test_wait_for_read(self):
    """ Tests that the wait_for_read method works. """
    # If the box is empty, it should return immediately.
    self.test_box.wait_for_read()

    # Now, do a simple multiprocessed test.
    self.test_box.set("potentialize")

    process = self.TestingProcess(self.test_box)
    process.start()

    self.assertEqual("potentialize", self.test_box.get())
    process.join()
    self.assertEqual("meritocracy", self.test_box.get())
