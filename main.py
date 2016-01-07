#!/usr/bin/python


import multiprocessing
import logging
import os

#from Utils.log_writer import LogWriter
from Utils.messaging import Messenger
from Utils.process import Process
from Utils import nr_logger


def run_processes(messenger, logger):
  """ Run all the processes, and restart any that die.
  Args:
    messenger: The messenger to use for IPC.
    logger: The logger to use for logging. """
  # These have to be imported here, after the logging system has been properly
  # initialized.
  from BeliefSystem.aggregator import Aggregator
  from BeliefSystem.belief_manager import BeliefManager

  processes = []
  processes.append(nr_logger.LogWriter(messenger.get_queue("logging"), "NRLog"))
  processes.append(Aggregator(messenger.get_queue("uavStatus"),
                              messenger.get_queue("fromRadio"),
                              messenger.get_queue("toBelief")))
  # TODO (danielp): Add real wireless queue when we want that feature.
  processes.append(BeliefManager(messenger.get_queue("toBelief"),
                                 None))

  #TODO: spawn RadioListener, MAVLink
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

  # Set up logging (This has to happen before anyone uses a logger.)
  nr_logger.QueueLogger.set_queue(messenger.get_queue("logging"))

  # Configure our logger.
  logger = logging.getLogger('Core')
  logger.info('System starting...')

  try:
    run_processes(messenger, logger)
  except Exception as e:
    logger.critical("Core: %s" % (e,))
    raise

  logger.critical("Core exiting!")


if __name__ == "__main__":
  main()
