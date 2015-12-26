""" Standard shared utilities. """


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
