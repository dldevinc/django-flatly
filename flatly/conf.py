from django.conf import settings


ENGINE = getattr(settings, 'FLATLY_ENGINE', None)
TEMPLATE_ROOT = getattr(settings, 'FLATLY_TEMPLATE_ROOT', None)
EXTENSIONS = getattr(settings, 'FLATLY_EXTENSIONS', ['html'])
