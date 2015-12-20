from multiprocessing import Array, Value
import cPickle as pickle
import logging
import sys


class Messenger(object):
  """
    Manages messaging between local processes
  """

  class Queues(object):
    """
      Enum for messenger queues
    """
    uavStatus = 'uavStatus'
    toBelief = 'toBelief'
    fromRadio = 'fromRadio'

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
      self.__logger = logging.getLogger('SingleQueue[' + name + ']')
      self.__logger.debug('Initialized SingleQueue')

    def __clear_queue(self):
      if not self.__used.value:
        self.__logger.warn('Tried to clear empty queue')
        return

      self.__used.value = 0

    def set(self, obj):
      if self.__used.value:
        self.__logger.debug('Queue has not been read')
        self.__clear_queue()

      # Pickle the data and write it in.
      pickled = pickle.dumps(obj)
      if len(pickled) > self._SIZE:
        self.__logger.critical("Object of size %d exceeds maximum size of %d!" \
                               % (len(pickled), self._SIZE))
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
    self._queue_map[self.Queues.uavStatus] = self.Mailbox(self.Queues.uavStatus)
    self._queue_map[self.Queues.toBelief] = self.Mailbox(self.Queues.toBelief)
    self._queue_map[self.Queues.fromRadio] = self.Mailbox(self.Queues.fromRadio)

  def get_queue(self, queue_name):
    return self._queue_map[queue_name]
