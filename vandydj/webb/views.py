import os
import urllib, json

import cv2
import numpy as np
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
from fastai.basic_train import load_learner
from fastai.vision import Learner, pil2tensor
from fastai.vision import Image as fImage
from vandydj.webb.forms import ImageUploadForm


class UploadImageView(TemplateView):
    template_name = 'webb/image_upload.html'

    def get(self, request, *args, **kwargs):
        img_form = ImageUploadForm()
        return self.render_to_response({
            'form': img_form
        })

    def post(self, request, *args, **kwargs):
        img_form = ImageUploadForm(request.POST, request.FILES)
        if img_form.is_valid():
            print("Hello")
            # form_img = request.FILES['image'].image
            form_img = img_form.cleaned_data['image'].image
            #form_img = form_img.convert('RGB')
            #frame = cv2.cvtColor(form_img, cv2.COLOR_BGR2RGB)
            #frame = cv2.resize(frame, (224, 224))
            #frame_fastai = fImage(pil2tensor(frame, dtype=np.float32).div_(255))
            import ipdb;ipdb.set_trace()
            prob, label = self.get_classified_prob(form_img)
            return JsonResponse({
                'Predicted label': label,
                'Predicted Prob': prob
            })
        else:
            return self.render_to_response({
                'form': img_form
            })

    @staticmethod
    def get_classified_prob(img):
        learn: Learner = load_learner(
            path=os.path.join(settings.BASE_DIR, 'vandydj/ai_models/'), file='model_v1.pkl'
        )
        prediction = learn.predict(img)
        label = prediction[0]
        prob = max(prediction[2])
        return prob, label

    @staticmethod
    def get_classified_gif(label):
        data = json.loads(
            urllib.urlopen("http://api.giphy.com/v1/gifs/search?q=f'{label}'&api_key=YOUR_API_KEY&limit=1").read())
        print(json.dumps(data, sort_keys=True, indent=4))