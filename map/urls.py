from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path('test/', views.test),
        path('tracker/last_active', views.getLastActive),
        path('locations', views.getLocationBySpan),
        path('real_time/test', views.sse_test),
        path('real_time/simulate', views.sse),
]