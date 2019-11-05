from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from vandydj.webb.views import UploadImageView, GetGiffyView

urlpatterns = [
    path("get_gif_url", csrf_exempt(GetGiffyView.as_view()), name='get_giffy'),
    path("", UploadImageView.as_view(), name='image_upload'),
]

