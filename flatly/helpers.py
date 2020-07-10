import posixpath
from django.template.base import Origin
from django.template.loader import _engine_list
from django.template.backends.django import copy_exception
from django.template.exceptions import TemplateDoesNotExist
from .exceptions import InvalidTemplatePath
from . import conf

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
        if (not path.startswith(base + posixpath.sep) and
                path != base):
            raise InvalidTemplatePath(path)

    return path


def check_template_variants(engine, name):
    tried = []

    # check direct path
    try:
        template = engine.get_template(name)
    except TemplateDoesNotExist as e:
        tried.extend(e.tried)
    except IsADirectoryError:
        tried.append((
            Origin(name, name, engine),
            'Source does not exist'
        ))
    else:
        return template

    # check extensions
    for ext in conf.EXTENSIONS:
        name_with_extension = '.'.join([name, ext])

        try:
            template = engine.get_template(name_with_extension)
        except TemplateDoesNotExist as e:
            tried.extend(e.tried)
        except IsADirectoryError:
            tried.append((
                Origin(name_with_extension, name_with_extension, engine),
                'Source does not exist'
            ))
        else:
            return template

    # check inner "index" file
    for ext in conf.EXTENSIONS:
        index_file = posixpath.join(name, 'index.{}'.format(ext))

        try:
            template = engine.get_template(index_file)
        except TemplateDoesNotExist as e:
            tried.extend(e.tried)
        except IsADirectoryError:
            tried.append((
                Origin(index_file, index_file, engine),
                'Source does not exist'
            ))
        else:
            return template

    raise TemplateDoesNotExist(name, tried=tried, backend=engine)


def get_template_by_name(name: str):
    """
    Search path for "/news/article":
        1) /templates/news/article
        2) /app/templates/news/article
        3) /templates/news/article.html
        4) /app/templates/news/article.html
        5) /templates/news/article/index.html
        6) /app/templates/news/article/index.html
    """
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
            template = check_template_variants(engine, name)
        except TemplateDoesNotExist as e:
            chain.append(e)
        else:
            template_cache[name] = template
            return template

    exception = TemplateDoesNotExist(name, chain=chain)
    template_cache[name] = copy_exception(exception)
    raise exception
