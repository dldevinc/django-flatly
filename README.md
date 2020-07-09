# django-flatly
Serving flat pages with Django without applications and views

## Installation
`pip install django-flatly`

Add a URL to urlpatterns (**MUST be the last route!**)
```python
# urls.py
urlpatterns = [
    ...,
    # Django >= 2.0
    path('', include('flatly.urls')),
    
    # Django < 2.0
    url(r'', include('flatly.urls')),
]
```
