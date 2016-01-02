""" Standard shared utilities. """


from collections import deque
import Queue

import time


class PhasedLoopLimitter:
  """ Constrains a loop to running a particular number of iterations per second.
  """

  def __init__(self, rate):
    """ Args:
      rate: How much time should elapse between each cycle. """
    self.__ticks = rate
    self.__last_run_time = 0

  def set_rate(self, rate):
    """ Sets the target rate for this loop.
    Args:
      rate: How much time should elapse between each cycle. """
    self.__ticks = rate

  def limit(self):
    """ Should be called every iteration of a loop. It checks that the proper
    amount of time has passed and delays execution until it has.
    Args:
      rate: The target number of iterations per second. """
    new_time = self.__do_limit()
    self.__last_run_time = new_time

  def __do_limit(self):
    """ Only does the waiting, does not update __last_run_time.
    Returns:
      The time it got when it started. """
    new_time = time.time()
    elapsed = new_time - self.__last_run_time
    sleep_for = max(0, self.__ticks - elapsed)
    time.sleep(sleep_for)
    return new_time


class TestQueue:
  """ Real Python queues are not strongly consistent with puts, which makes them
  somewhat impractical for testing purposes. Therefore, here we have a stupid
  little class that has the same API as a real queue, but just buffers data for
  testing purposes.
  NOTE: Because it is meant to be used in a single-threaded environment,
  blocking doesn't make sense at all. That means reading from an empty TestQueue
  will just throw an exception. Because of this, blocking arguments are provided
  for compatibility, but are all no-ops. """

  def __init__(self):
    # This is what actually stores data.
    self.__buffer = deque()

  def put(self, item, block=True):
    """ Puts an item on the fake queue.
    Args:
      item: The item to put.
      block: No-op. """
    self.__buffer.appendleft(item)

  def put_nowait(self, item):
    self.put(item, block=False)

  def get(self, block=True):
    """ Removes an item from the fake queue. Reading from an empty queue raises
    a Queue.Empty exception.
    Args:
      block: no-op.
    Returns:
      The item that was removed. """
    if not len(self.__buffer):
      raise Queue.Empty()

    return self.__buffer.pop()

  def get_nowait(self):
    return self.get(block=False)

  def empty(self):
    """ Checks whether the fake queue is empty or not.
    Returns:
      True if the queue is empty, False otherwise. """
    return not len(self.__buffer)

  def clear(self):
    """ Removes everything in the queue. """
    self.__buffer = deque()
