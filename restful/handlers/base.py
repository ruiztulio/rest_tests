import tornado.web
from tornado.options import (define, options)
import json
import logging

class BaseHandler(tornado.web.RequestHandler):

    @property
    def cursor(self):
        return self.application.cur

    def _send_response(self, res):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res))
        self.finish()
