import posixpath
from django.conf import settings
from django.http import Http404, HttpResponse
from django.template.exceptions import TemplateDoesNotExist
from . import conf
from .helpers import safe_join, get_template_by_name


def serve(request, path):
    path = posixpath.normpath(path).lstrip('/')
    path = path.replace('-', '_')

    if conf.TEMPLATE_ROOT:
        template_name = safe_join(path, conf.TEMPLATE_ROOT)
    else:
        template_name = posixpath.normpath(path)

    try:
        template = get_template_by_name(template_name)
    except TemplateDoesNotExist:
        if not settings.DEBUG:
            raise Http404
        raise

    content = template.render({}, request)
    return HttpResponse(content)
