import json
import os
import urllib
import requests
import random
import urllib.parse

import cv2
import numpy as np
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings
from django.template.response import TemplateResponse
from django.core.cache import cache

from fastai.basic_train import load_learner
from fastai.vision import Learner, pil2tensor
from fastai.vision import Image as fImage
from vandydj.webb.forms import ImageUploadForm
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class UploadImageView(TemplateView):
    template_name = 'webb/image_upload.html'

    def get(self, request, *args, **kwargs):
        img_form = ImageUploadForm()
        scopes = ['user-read-playback-state', 'user-read-private', 'streaming', 'user-modify-playback-state',
                  "user-read-email"]
        client_id = '4e768c3147be43a982ecc1745d9aa6ae'
        client_secret = 'b99d01f83963438dab542cba61a202f2'
        redirect_uri = 'http://localhost:8000/'
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                              scope=scopes, state='test')
        if ('code' not in request.GET) and ('error' not in request.GET):

            authorization_url, state = oauth.authorization_url(
                'https://accounts.spotify.com/authorize',
                # access_type and prompt are Google specific extra
                # parameters.
                access_type="offline", prompt="select_account")
            return HttpResponseRedirect(authorization_url)

        elif 'code' in request.GET:
            code = request.GET['code']
            token = oauth.fetch_token(
                'https://accounts.spotify.com/api/token',
                code=code,
                client_secret=client_secret
            )
            cache.set('token', token['access_token'])
            return self.render_to_response({
                'form': img_form
            })
        else:
            return JsonResponse({'msg': "user didn't authorize the device!!"})

    def post(self, request, *args, **kwargs):
        access_token = cache.get('token')
        img_form = ImageUploadForm(request.POST, request.FILES)
        if img_form.is_valid():
            form_img = img_form.cleaned_data['image'].image
            prob, label = self.get_classified_prob(form_img)
            prediction_label = str(label)
            prediction_prob = float(prob)
            uri_set = self.get_recommended_tracks(prediction_label, prediction_prob, access_token)

            return TemplateResponse(
                request=self.request,
                template='webb/spotify_player.html',
                context={
                    'uri_set': uri_set[0] or '',
                    'access_token': access_token
                },
                **{'content_type': 'text/html'}
            )
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

    @staticmethod
    def get_tag_from_prediction(prediction_label, prediction_prob):
        if float(prediction_prob) < 0.3:
            prediction_label = 'default'

        song_tags = {'birthday': ['Birthday Songs', 'Happy Birthday (Birthday Song Collection)'],
                     'christmas': ['Christmas Peaceful Piano', 'Christmas Pop', 'Christmas'],
                     'halloween': ['Halloween monster jams', 'Stay Scary', 'Halloween Party', 'Ultimate Halloween',
                                   'Halloween Teens', 'Halloween Sound Effects', 'Halloween Horror',
                                   "Halloween's Gravest Hits"],
                     'party': ['Bass Drop', 'Dance Party', 'Dance Hits'],
                     'wedding': ['Wedding', 'Wedding Aisle Music', 'Wedding Reception Music: The Way You Look Tonight']
                     }
        return song_tags.get(prediction_label, '')

    def get_recommended_tracks(self, prediction_label, prediction_prob, access_token):
        tag = self.get_tag_from_prediction(prediction_label, prediction_prob) or []
        search_term = urllib.parse.quote(' OR '.join(tag))
        uri_set = set()
        for t in tag:
            rs = requests.get(
                f"https://api.spotify.com/v1/search?q={t}&type=track&limit=25&market=US",
                headers={'Authorization': f"Bearer {access_token}"}
            )
            if rs.status_code != 200:
                continue
            else:
                songs = rs.json()['tracks']['items']
                song_uris = list(map(lambda r: r['uri'], songs))
                uri_set.update(song_uris)
        uri_set = list(uri_set)
        random.shuffle(uri_set)
        return uri_set
