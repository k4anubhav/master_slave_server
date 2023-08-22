from django.urls import path

from .views import *

urlpatterns = [
    path('job/', CreateJobView.as_view(), name='job'),
    # get yourself job assigned
    path('job/get-assigned/', GetJobAssignedView.as_view(), name='get-assigned-job'),
    path('job/result/', CreateJobResultView.as_view(), name='job-result'),
    path('ping/', PingView.as_view(), name='ping'),
]
