import socket
import struct

class UdpSender:
  def __init__(self, host='127.0.0.1', port='4242'):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.host = host
    self.port = port

  def send_opentrack(self, pose):
    data = struct.pack("dddddd", pose[0], pose[1], pose[2], pose[3], pose[4], pose[5])
    self.socket.sendto(data, (self.host, self.port))

  def send_vjoy(self, pose):
    data = struct.pack("hhhhhhhHHI", pose[0], pose[1], pose[2], pose[3], pose[4], pose[5], pose[6], pose[7],pose[8],pose[9])
    self.socket.sendto(data, (self.host, self.port))

