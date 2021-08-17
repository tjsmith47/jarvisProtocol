from django.conf import settings
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('', include('users_app.urls')),
    path('debug/', include(debug_toolbar.urls)),
]
