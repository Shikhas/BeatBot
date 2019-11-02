from django.http import HttpResponse
from django.views.generic import TemplateView


class UploadImageView(TemplateView):
    template_name = 'webb/image_upload.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(content=b'Hello this would display the inference from the model')
