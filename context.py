
class Context:

  @staticmethod
  def parse_request_string(req):
    return {
      "method": req.split(None, 1)[0]
    }

  def __init__(self, req_str):
    self.req = Context.parse_request_string(req_str.decode('utf-8'))
    self.res = {}

  def to_HTTP(self):
    res = b'\n\r'.join([
      b"HTTP/1.0 200 OK",
      b"Content-Type: text/html",
      b"X-Powered-By: ccutch",
      b"",
      b"""
        <html>
          <h1>This is a test message</h1>
        </html>
      """
    ])
    return res
    # return res.encode('utf-8') => for string to bytes
