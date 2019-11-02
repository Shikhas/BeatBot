import os

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from fastai.basic_train import load_learner
from fastai.vision import Learner

class UploadImageView(TemplateView):
    template_name = 'webb/image_upload.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(content=b'Hello this would display the inference from the model')

    def get_classified_prob(self, img):
        learn: Learner = load_learner(
            path=os.path.join(settings.BASE_DIR, 'vandydj/ai_models/'), file='model_v1.pkl'
        )
        prediction = learn.predict(img)
        label = prediction[0]
        # print(label)
        prob = max(prediction[2])
        return prob, label
