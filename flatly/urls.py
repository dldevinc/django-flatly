from django.urls import re_path
from .views import serve


app_name = 'flatly'
urlpatterns = [
    re_path(r'^(?P<path>.*)$', serve),
]
