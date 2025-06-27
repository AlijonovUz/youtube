from django.urls import path

from .views import *

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('audio/', AudioDownloadView.as_view(), name='audio_download'),
    path('video/formats/', VideoFormatsView.as_view(), name='video_formats'),
    path('video/download/', VideoDownloadView.as_view(), name='video_download'),
]