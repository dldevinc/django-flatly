import posixpath

from django.template.backends.django import copy_exception
from django.template.base import Origin
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import _engine_list

from . import conf
from .exceptions import InvalidTemplatePath

template_cache = {}


def safe_join(path, base=None):
    """
    Join path components intelligently.
    Return a normalized version of the template path.
    """
    path = posixpath.normpath(path)
    base = base.strip().strip('/') if base is not None else None

    if base:
        path = posixpath.normpath(posixpath.join(base, path))

        # prevent "../" tricks
        if not path.startswith(base + posixpath.sep) and path != base:
            raise InvalidTemplatePath(path)

    return path


def _check_template_file(engine, name, tried):
    try:
        return engine.get_template(name)
    except TemplateDoesNotExist as e:
        tried.extend(e.tried)
    except IsADirectoryError:
        tried.append((Origin(name, name, engine), 'Source does not exist'))


def check_possible_template_paths(engine, name):
    """
    Search path for "/news/article":
        1) /templates/news/article
        2) /templates/news/article.html
        3) /templates/news/article/index.html
    """
    tried = []

    # check direct path
    template = _check_template_file(engine, name, tried)
    if template is not None:
        return template

    # check extensions
    for ext in conf.EXTENSIONS:
        template_name_with_extension = '.'.join([name, ext])
        template = _check_template_file(engine, template_name_with_extension, tried)
        if template is not None:
            return template

    # check inner "index" file
    for ext in conf.EXTENSIONS:
        index_template_name = posixpath.join(name, 'index.{}'.format(ext))
        template = _check_template_file(engine, index_template_name, tried)
        if template is not None:
            return template

    raise TemplateDoesNotExist(name, tried=tried, backend=engine)


def get_template_by_name(name: str):
    cached = template_cache.get(name)
    if cached:
        if isinstance(cached, type):
            if issubclass(cached, TemplateDoesNotExist):
                raise cached(name)
            else:
                raise cached()
        elif isinstance(cached, TemplateDoesNotExist):
            raise copy_exception(cached)
        return cached

    chain = []
    engines = _engine_list(conf.ENGINE)
    for engine in engines:
        try:
            template = check_possible_template_paths(engine, name)
        except TemplateDoesNotExist as e:
            chain.append(e)
        else:
            template_cache[name] = template
            return template

    exception = TemplateDoesNotExist(name, chain=chain)
    template_cache[name] = copy_exception(exception)
    raise exception
