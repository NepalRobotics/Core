import multiprocessing as mp


class Process(object):
  """ This class represents a single process running on the system. It is
  designed to interact well with Python's multiprocessing tools. """

  def __init__(self):
    """ Args:
      messenger: The messenger object that we are using. """
    # The actual process object.
    self.__process = None

  def _run(self):
    """ Do the stuff that this process needs to do. Meant to be overridden by
    the user. """
    pass

  def start(self):
    """ Takes care of any initialization and starts the process.
    Returns: The PID of the started process. """
    if self.__process:
      # We died, and we're being restarted.
      self.__process.join()

    self.__process = mp.Process(target=self._run)
    self.__process.start()

    return self.__process.pid
