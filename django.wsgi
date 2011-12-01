import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
#sys.path.append('/Users/bi2one/public_html')
#sys.path.append('/Users/bi2one/public_html/worry')

os.environ['DJANGO_SETTINGS_MODULE'] = 'worry.settings'

from django.core.servers.fastcgi import runfastcgi
runfastcgi([method="threaded", daemonize="false"])

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

