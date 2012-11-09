
import urllib
import urllib2
import json
url = "http://localhost:8888/login?login=usuario&pswd=202cb962ac59075b964b07152d234b70"

req = urllib2.Request(url)
response = urllib2.urlopen(req)
print response.headers
the_page = response.read()

print the_page

info = json.loads(the_page)

print info
