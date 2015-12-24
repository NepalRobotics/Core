#!/usr/bin/python


import multiprocessing
import logging
import os

from messaging import Messenger
from process import Process
import nr_logger


def run_processes(messenger, logger):
  """ Run all the processes, and restart any that die.
  Args:
    messenger: The messenger to use for IPC.
    logger: The logger to use for logging. """
  processes = []
  processes.append(nr_logger.LogWriter(messenger.get_queue("logging"),
                                       "NRLog"))

  #TODO: spawn BeliefSystem, RadioListener, MAVLink
  #TODO: start processes

  # Start all the processes.
  logger.info("Starting processes.")
  pids = {}
  for process in processes:
    pid = process.start()
    pids[pid] = process

  # Restart any processes that die.
  while True:
    # Wait for any child process.
    pid, status = os.waitpid(-1, 0)
    if status != 0:
      logger.warning("Process %d exited unexpectedly! Restarting..." % (pid))
      process = pids.pop(pid)
      new_pid = process.start()
      pids[new_pid] = process

def main():
  messenger = Messenger()

  # This has to happen before anyone uses a logger.
  nr_logger.QueueLogger.set_queue(messenger.get_queue("logging"))

  # Configure our logger.
  logger = logging.getLogger('Core')
  logger.info('System starting...')

  try:
    run_processes(messenger, logger)
  except Exception as e:
    logger.critical("Core: %s" % (e,))

  logger.critical("Core exiting!")


if __name__ == "__main__":
  main()
