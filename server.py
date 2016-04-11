"""
A simple implementation of a web server using asyncio libraries with python3.5
"""

import socket
import asyncio
from context import Context



class Server:

  max_connections = 10
  client = None
  server = None

  def __init__(self, addr="0.0.0.0", port=3000):
    self.is_open = False
    self.client = None
    self.addr = addr
    self.port = port
    self.middleware = []

  def _open(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind((self.addr, self.port))
    self.socket.listen(self.max_connections)

  def _close(self):
    self._clean_client_connections()
    if self.socket:
      self.socket.close()

  def _clean_client_connections(self):
    if self.client:
      self.client.close()
      self.client = None

  def _read(self, size=1024):
    self._clean_client_connections()
    self.client, _ = self.socket.accept()
    return self.client.recv(size)

  def _send(self, msg):
    if not self.client:
      raise Exception("No client connected")
    self.client.send(msg)

  def _wait_for_connection(self):
    if self.socket != None:
      raise Exception("Socket is not open.")

  async def listen(self):
    # Start listening for incoming request on tcp socket
    self._open()
    while True:
      req = self._read()
      if not req:
        break
      ctx = Context(req)
      # This should run middleware in parallel?
      for fn in self.middleware:
        await fn(ctx)
      self._send(ctx.to_HTTP())

  def listen_sync(self):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.listen())
    loop.close()





if __name__ == "__main__":
  server = Server()
  server.listen_sync()
