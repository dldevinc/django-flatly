from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('tests.app.urls')),
    path('', include('flatly.urls')),
]
