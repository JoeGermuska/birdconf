from birdconf.configs.common.settings import *

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database
DATABASE_HOST = 'db.tribapps.com'
DATABASE_PORT = '5433'
DATABASE_USER = 'birdconf'
DATABASE_PASSWORD = 'Ad43pDchrJ'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.tribapps.com/birdconf/'

# Predefined domain
MY_SITE_DOMAIN = 'birdconf.tribapps.com'

# Email
EMAIL_HOST = 'mail.tribapps.com'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://memcache.tribapps.com:11211/'

# S3
AWS_S3_URL = 's3://media.tribapps.com/birdconf/'

# Google Maps for all chicagotribune.com
GOOGLE_MAPS_API_KEY = "ABQIAAAA3uGjGrzq3HsSSbZWegPbIhR5COEpVyQUV9kv-lkpbZNYiwcxghT6I7X0aBuunZEEDZxFYYtK5nhTuA"

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)