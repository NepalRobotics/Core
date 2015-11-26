#!/usr/bin/python

import multiprocessing
from MAVLinkConnector.mav_link_connector import MavLinkConnector
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s %(name)s: %(message)s',
    filename='NRLog', level=logging.DEBUG)
logger = logging.getLogger('Core')

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

  class SingleQueue(object):
    """
      Lockable queue with only one element
    """

    def __init__(self, name):
      self.__queue = multiprocessing.Queue(1)
      self.__logger = logging.getLogger('SingleQueue[' + name + ']')
      self.__logger.debug('Initialized SingleQueue')
    
    def __clear_queue(self):
      try:
        self.__queue.get(False)
      except multiprocessing.Queue.Empty:
        self.__logger.warn('Tried to clear empty queue')

    def set(self, obj):
      if self.__queue.empty() == False:
        self.__logger.debug('Queue has not been read')
        self.__clear_queue
      self.__queue.put(obj)

    def get(self):
      if self.__queue.empty():
        return None
      return self.__queue.get()


  def __init__(self):
    self._queue_map = {}
    # Set up lockable data structures for local belief generation
    self._queue_map[self.Queues.uavStatus] = self.SingleQueue(self.Queues.uavStatus)
    self._queue_map[self.Queues.toBelief] = self.SingleQueue(self.Queues.toBelief)
    self._queue_map[self.Queues.fromRadio] = self.SingleQueue(self.Queues.fromRadio)

  def _gather_sensors(self):
    """
      Collect data to send to belief system (and eventually logs/wifi)
    """
    # Get latest data from radio and MAV processes
    sensor_status = {'CraftData': self._queue_map[self.Queues.uavStatus].get(),
                     'RadioData': self._queue_map[self.Queues.fromRadio].get()}
    # Send collected data to belief generation process
    self._queue_map[self.Queues.toBelief].set(sensor_status)

    logger.debug('Gathered status', sensor_status)

    # TODO: send to logging process

  def run(self):
    """
      Main loop
    """
    while True:
      self._gather_sensors()

  def get_queue(self, queue_name):
    return self._queue_map[queue_name]

if __name__ == '__main__':
  logger.info('System starting')
  messenger = Messenger()
  logger.debug('Messenger finished initializing')

  mavLink = MavLinkConnector(messenger.get_queue(Messenger.Queues.uavStatus))
  logger.debug('MAV Link connector spawned')
