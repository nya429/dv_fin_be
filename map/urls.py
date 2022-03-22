from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path('test/', views.test),
        path('tracker/last_active', views.getLastActive),
        path('locations', views.getLocationBySpan),
]