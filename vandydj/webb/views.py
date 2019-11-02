from django.http import HttpResponse
from django.views.generic import TemplateView
from fastai import *
from fastai.vision import *

class UploadImageView(TemplateView):
    template_name = 'webb/image_upload.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(content=b'Hello this would display the inference from the model')

    def get_classified_prob(image):
        learn = load_learner(path=str(base_path / 'cohort_models/'), file='childproof_electrical_chicago.pkl')
        prediction = learn.predict(image)
        label = prediction[0]
        # print(label)
        prob = max(prediction[2])
        return prob, label
