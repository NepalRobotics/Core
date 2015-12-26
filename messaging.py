from multiprocessing import Array, Queue, Value
import cPickle as pickle
import sys


class Messenger(object):
  """
    Manages messaging between local processes

    NOTE: Logging cannot be used here because the logging system relies on
    Messenger.
    NOTE: Messenger is intended to be used by the main process only.
  """

  class Queues(object):
    """
      Enum for messenger queues
    """
    uavStatus = 'uavStatus'
    toBelief = 'toBelief'
    fromRadio = 'fromRadio'
    logging = 'logging'

  class Mailbox(object):
    """
      A lock-protected bit of shared state that can be used to send a single
      value between processes. Thanks to Pickle, it can store pretty much
      anything.
    """

    # The size of the array that stores data.
    _SIZE = 1024

    def __init__(self, name):
      # Where we write the element.
      self.__state = Array('c', self._SIZE)
      # Whether the slot is in use. If it's not, it's zero, otherwise it's the
      # length of whatever's in it.
      self.__used = Value('i', 0)

    def __clear_queue(self):
      if not self.__used.value:
        return

      self.__used.value = 0

    def set(self, obj):
      if self.__used.value:
        self.__clear_queue()

      # Pickle the data and write it in.
      pickled = pickle.dumps(obj)
      if len(pickled) > self._SIZE:
        print "Object of size %d exceeds maximum size of %d!" % \
              (len(pickled), self._SIZE)
        sys.exit(1)

      self.__state.value = pickled
      self.__used.value = len(pickled)

    def get(self):
      if not self.__used.value:
        return None

      # Get the pickled item.
      pickled = self.__state.value
      pickled = pickled[:self.__used.value]
      self.__used.value = 0

      return pickle.loads(pickled)


  def __init__(self):
    self._queue_map = {}
    # Set up lockable data structures for local belief generation
    self._queue_map[self.Queues.uavStatus] = Queue()
    self._queue_map[self.Queues.toBelief] = self.Mailbox(self.Queues.toBelief)
    self._queue_map[self.Queues.fromRadio] = Queue()

    self._queue_map[self.Queues.logging] = Queue()

  def get_queue(self, queue_name):
    return self._queue_map[queue_name]
