""" Tests for messaging.py. """


import unittest

import messaging


class TestMailbox(unittest.TestCase):
  """ Tests for the Mailbox class. """

  def setUp(self):
    self.test_box = messaging.Messenger.Mailbox("testBox")

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
