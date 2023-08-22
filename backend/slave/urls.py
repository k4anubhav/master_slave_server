from django.urls import path

from .views import *

urlpatterns = [
    path('token/', SlaveViewSet.as_view({'post': 'create'}), name='token'),
    path('token/regenrate/', SlaveViewSet.as_view({'post': 'regenerate'}), name='token-regenerate'),
]
