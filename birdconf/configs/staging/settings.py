from birdconf.configs.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
DATABASE_HOST = 'db.beta.tribapps.com'
DATABASE_PORT = '5433'
DATABASE_USER = 'birdconf'
DATABASE_PASSWORD = 'Ad43pDchrJ'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media-beta.tribapps.com/birdconf/'

# Predefined domain
MY_SITE_DOMAIN = 'birdconf.beta.tribapps.com'

# Email
EMAIL_HOST = 'mail.beta.tribapps.com'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://memcache.beta.tribapps.com:11211/'

# S3
AWS_S3_URL = 's3://media-beta.tribapps.com/birdconf/'

# Google Maps for all tribapps.com
GOOGLE_MAPS_API_KEY = "ABQIAAAA3uGjGrzq3HsSSbZWegPbIhSLxTlal1xvdPXu2siN6MQ6NGGqkRTeTxuPzPKHY8_Bz37fpLDMQBrL6A"

# Trib IPs for security
INTERNAL_IPS = ('163.192.12.84','163.192.12.108','163.192.12.32')

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)