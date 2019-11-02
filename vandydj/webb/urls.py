from django.urls import path

from vandydj.webb.views import UploadImageView

urlpatterns = [
    path("", UploadImageView.as_view(), name='index'),
]