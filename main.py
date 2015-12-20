#!/usr/bin/python


import multiprocessing
import logging
import os

from messaging import Messenger
from process import Process


# Configure logging
logging.basicConfig(format='%(asctime)s %(name)s: %(message)s',
    filename='NRLog', level=logging.DEBUG)
logger = logging.getLogger('Core')


def main():
  logger.info('System starting')
  messenger = Messenger()
  logger.debug('Messenger finished initializing')

  processes = {}

  #TODO: spawn BeliefSystem, RadioListener, MAVLink
  #TODO: start processes

  # Restart any processes that die.
  while True:
    # Wait for any child process.
    pid, status = os.waitpid(-1, 0)
    if status != 0:
      logger.warning("Process %d exited unexpectedly! Restarting..." % (pid))
      processes[pid].start()


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    logger.critical("Core: %s" % (e))

  logger.critical("Core exiting!")
