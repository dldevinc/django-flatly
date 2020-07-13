# django-flatly
Serving flat pages with Django without views and database.

Helps to separate deployment of front- and backend.

![](https://travis-ci.org/dldevinc/django-flatly.svg?branch=master)

## Installation
Install the latest release with pip:

`pip install django-flatly`

Than add a URL to urlpatterns:
```python
# urls.py
urlpatterns = [
    ...,
    # all others urls above - flatly.urls last one to try!
    path('', include('flatly.urls')),
]
```

## Quick start

1) In your root template directory create `flatly` folder.

2) Define `FLATLY_TEMPLATE_ROOT` setting:
    ```python
    FLATLY_TEMPLATE_ROOT = 'flatly'
    ```

3) Any `.html` files you create in your `flatly` directory
will be automatically served. So if you create a new file
`flatly/about_us/overview.html` then it will be visible at
`/about-us/overview/`.

Note that `django-flatly` automatically replaces underscores (_)
with dashes (-).

## Search path

Suppose you are requesting the page `/account/user-profile/`,
`django-flatly` will render the first template that exists:
1) `${FLATLY_TEMPLATE_ROOT}/account/user_profile`
2) `${FLATLY_TEMPLATE_ROOT}/account/user_profile.html`
3) `${FLATLY_TEMPLATE_ROOT}/account/user_profile/index.html`

## Settings

### Template root
`django-flatly` based on Django's `get_template` function.
So, any user can access any template on your website. You can
restrict access to certain templates by adding the following:

```python
FLATLY_TEMPLATE_ROOT = 'flatly'
```

By adding the above configuration `django-flatly` will add
specified path prefix to the template name before search.

Suppose you are requesting the page `/account/user/`,
`django-flatly` will call something like
```get_template('flatly/account/user.html')```.

Note that `flatly` folder can be located in both root and
application template directories.

Defaults to `None`.

### Template engine
You can restrict the template search to a particular template engine.

```python
FLATLY_ENGINE = 'jinja2'
```

Defaults to `None`.

### Extensions
List of file extensions to iterate over all matching files.
```python
FLATLY_EXTENSIONS = ['html', 'jinja2']
```
Defaults to `html`.

## Development and Testing
After cloning the Git repository, you should install this
in a virtualenv and set up for development:
```shell script
virtualenv .venv
source .venv/bin/activate
pip install -r ./requirements_dev.txt
pre-commit install
```
