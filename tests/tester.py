#!/usr/bin/python

import threading
import time
import urllib
import urllib2

exitFlag = 0
url = "http://openerp.localhost"

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        # self._metodos = ['/clients/', '/products/', '/sales']
        self._metodos = ['/']
        threading.Thread.__init__(self)

    def run(self):
        for i in xrange(1000):
            for metodo in self._metodos:
                req = urllib2.Request(url+metodo)
                response = urllib2.urlopen(req)
                the_page = response.read()


# Se crea el pool de hilos
threads = [myThread(i, "Thread-%s"%i, i) for i in xrange(20)]

# los ejecutamos
for thr in threads:
    thr.start() 
