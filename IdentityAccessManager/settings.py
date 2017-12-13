"""
Django deployment settings for IdentityAccessManager project.
"""

PRODUCTION = False


if PRODUCTION:
    try:
        from production_settings import *
    except ImportError:
        raise ImportError('The production_settings python file does not exist')
else:
    try:
        from dev_settings import *
    except ImportError:
        raise ImportError('The dev_settings python file does not exist')


LOGO_URL = MEDIA_URL +  "app/users/logos/"
LOGO_PATH = MEDIA_ROOT + "/app/users/logos/"