#!/usr/bin/env python
import os
import sys
reload sys
sys.setdefaultencoding('utf8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

import warnings
from django.core.cache import CacheKeyWarning
warnings.simplefilter("ignore", CacheKeyWarning)

from django.core.management import execute_from_command_line
if __name__ == "__main__":
    execute_from_command_line(sys.argv)