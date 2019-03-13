import os
import sys

path = '/home/manish2121/photographyadda'
if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'photographyadda.settings'

from django.core.wsgi import get_wsgi application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
