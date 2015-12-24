import logging
import time

from process import Process


class LogWriter(Process):
  """ Reads data from the logging queue and writes it to a file. """

  def __init__(self, queue, filename):
    """ Args:
      queue: The queue to read messages from.
      filename: The base file name to write log messages to. """
    super(LogWriter, self).__init__()

    self.__queue = queue

    # Use the current epoch time to make each new file unique.
    systime = int(time.time())
    self.__file = open("%s-%d.log" % (filename, systime), "a")

  def __del__(self):
    self.__file.close()

  def _run(self):
    # Keep reading messages and write them to the file.
    while True:
      try:
        message = self.__queue.get()
      except (KeyboardInterrupt, SystemExit):
        # If it dies, flush everything.
        self.__file.close()
        return

      self.__file.write("%s\n" % message)


class QueueLoggingHandler(logging.Handler):
  """ A special handler that dumps messages to the logging queue. """

  def __init__(self, queue):
    """ Args:
      queue: The queue to log to. """
    super(QueueLoggingHandler, self).__init__()

    self.__queue = queue

  def emit(self, record):
    """ Writes a new message.
    Args:
        record: The message to write. """
    try:
      message = self.format(record)
      self.__queue.put(message)

    except (KeyboardInterrupt, SystemExit):
      raise
    except:
      self.handleError(record)


class QueueLogger(logging.Logger):
  """ A logger subclass with some minor customizations. The main point is that
  it logs to a queue instead of a file directly. """

  # The queue that we will be logging to.
  _queue = None

  def __init__(self, name):
    """ Args:
        name: The name of this logger. """
    super(QueueLogger, self).__init__(name)

    # I like it configured a certain way, so we might as well do that here.
    self.setLevel(logging.DEBUG)

    # Log everything to the queue.
    handler = QueueLoggingHandler(self._queue)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter( \
        "%(asctime)s %(name)s: [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    self.addHandler(handler)

  @classmethod
  def set_queue(cls, queue):
    """ Sets the queue that we are logging to and configures the logger.
    Args:
      queue: The queue that is being logged to. """
    cls._queue = queue

  """ Logs at the critical level and aborts.
  message: The message to log. """
  def fatal(self, message, *args, **kwargs):
    self.critical(message, *args, **kwargs)
    sys.exit(1)


# Use this as the default logger.
logging.setLoggerClass(QueueLogger)
