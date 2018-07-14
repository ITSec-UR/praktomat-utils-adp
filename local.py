# Settings for deployment

# These settings are KIT-specific and derive some parts of the settings
# from the directory name.
#
# If you are not deploying on praktomat.cs.kit.edu you need to rewrite this file.

from os.path import join, dirname, basename
import re

PRAKTOMAT_PATH = '/var/www/Praktomat/'

PRAKTOMAT_ID = basename(dirname(PRAKTOMAT_PATH))

match = re.match(r'''
	(?:praktomat_)?
	(?P<algo1>algo1_)?
	(?P<cram>cram_)?
	(?P<birap>birap_)?
	(?P<tba>tba_)?
	(?P<mlfds>mlfds_)?
	(?P<pp>pp_)?
	(?P<iimb>iimb_)?
	(?P<year>\d+)_
	(?P<semester>WS|SS)
	(?P<abschluss>_Abschluss)?
	(?P<mirror>_Mirror)?
	''', PRAKTOMAT_ID, flags=re.VERBOSE)

SITE_NAME = 'Praktomat Lehrstuhl Kesdogan'
MIRROR = False

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# developmentserver.
BASE_HOST = 'https://praktomat.itsec.ur.de'
# BASE_PATH = '/' + PRAKTOMAT_ID + '/'
BASE_PATH = '/'

ALLOWED_HOSTS = [ '*' ]

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'

STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

TEST_MAXLOGSIZE=512

TEST_MAXFILESIZE=512

TEST_TIMEOUT=180

if "cram" in PRAKTOMAT_ID:
  TEST_TIMEOUT=600
  TEST_MAXMEM=200

if "birap" in PRAKTOMAT_ID:
  TEST_TIMEOUT=600

if "tba" in PRAKTOMAT_ID:
  TEST_TIMEOUT=600

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "PraktomatSupport/")


SANDBOX_DIR = join('/var/www/Praktomat/PraktomatSupport/SolutionSandbox/', PRAKTOMAT_ID)


ADMINS = [
  ('Praktomat', 'kesdogan.technik@ur.de')
]


if MIRROR:
	EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
	EMAIL_FILE_PATH = join(UPLOAD_ROOT, "sent-mails")
else:
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = "localhost"
	EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = "kesdogan.technik@ur.de"

DEBUG = False

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   'praktomat_1',
			'USER':   'praktomat',
			'PASSWORD': 'praktoPW',
			'HOST': '132.199.249.82',
			'PORT': '5432',
    }
}

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'

# Enable Shibboleth:
SHIB_ENABLED = False
REGISTRATION_POSSIBLE = True

# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = False

# Use docker to test submission
USESAFEDOCKER = True

# Various extra files and versions
CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle-5.7-all.jar'
JPLAGJAR = '/srv/praktomat/contrib/jplag.jar'
#JAVA_BINARY = 'javac-sun-1.7'
#JVM = 'java-sun-1.7'

# Our VM has 4 cores, so lets try to use them
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 6

# Finally load defaults for missing setttings.
import defaults
defaults.load_defaults(globals())
