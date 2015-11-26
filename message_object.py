"""
This module contains classes for sending/receiving encoded data over
IPC sockets.
"""

import json, inspect, time

class MessageObject(object):
  """
  Class representing an IPC message
  """
  def __init__(self):
    """
    Construct a new MessageObject object.

    Returns:
      A new instance of a message object
    """
    self.time_created = time.time()
  def primitives(self):
    """Return a serializable dictionary of self's contents

    Args:

    Returns:
        A dictionary of self's primitives
    """
    prim_dict = {}
    for key in self.__dict__:
      elem = self.__dict__[key]
      # We determine whether elem is a serializable object, or whether
      # we need to recursively call the primitives operator on a
      # MessageObject
      # NOTE: this assumes all but message objects are serializable, so
      # make sure to only use serializables or to override encode() when
      # making subclasses of MessageObject

      if MessageObject in inspect.getmro(type(elem)):
        prim_dict[key] = elem.primitives()
      else:
        prim_dict[key] = elem
    return prim_dict

  def encode(self):
    """
    Create an encoded version of self
    :return: Returns encoded self
    """
    return json.dumps(self.primitives())

class VehicleState(MessageObject):
  """
  Encodable UAV craft state information
  """
  def __init__(self, vehicle_uid, **kwargs):
    """Construct a new VehicleState object

    Args:
        vehicle_uid: a unique identifier string for the craft sending state
        **kwargs: Optional information

    Returns: returns nothing
    """
    MessageObject.__init__()
    self.vehicle_uid = vehicle_uid
    self.vehicle_is_armed = kwargs.get("vehicle_is_armed")
    self.attitude_pitch = kwargs.get("attitude_pitch")
    self.attitude_yaw = kwargs.get("attitude_yaw")
    self.attitude_roll = kwargs.get("attitude_roll")
    self.velocity_array = kwargs.get("velocity_array")
    self.airspeed = kwargs.get("airspeed")
    self.groundspeed = kwargs.get("groundspeed")
    self.gps_fix_type = kwargs.get("gps_fix_type")
    self.latitude = kwargs.get("latitude")
    self.longitude = kwargs.get("longitude")
    self.altitude_absolute = kwargs.get("altitude_absolute")
    self.altitude_relative = kwargs.get("altitude_relative")
    self.battery_level = kwargs.get("battery_level")

class RadioState(MessageObject):
  """
  Encodable Doppler Radio signal state information

  Args:
    lob: the signal's Line of Bearing
    strength: the signal strength metric
  """
  def __init__(self, lob, strength):
    MessageObject.__init__()
    # The LOB to the signal source.
    self.lob = lob
    # The strength of the signal.
    self.strength = strength

class LogEvent(MessageObject):
  """
  Encodable information for recording to system log
  """
  #TODO: implement
  pass
