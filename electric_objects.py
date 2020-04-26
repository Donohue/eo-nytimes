from bs4 import BeautifulSoup
import json
import random
import requests
import urllib

class ElectricObjects:
    base_url = 'https://www.electricobjects.com/'

    def __init__(self, username, password):
          self.username = username
          self.password = password

    def authenticity_token(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        results = soup.findAll('meta', {'name': 'csrf-token'})
        return results[0].attrs['content']

    def authenticate_session(self, session):
        sign_in_url = '%s/sign_in' % self.base_url
        r = session.get(sign_in_url)
        authenticity_token = self.authenticity_token(r.text)
        payload = {
            "user[email]": self.username,
            "user[password]": self.password,
            "authenticity_token": authenticity_token
        }
        return session.post(sign_in_url, data=payload)

    def make_request(self, url, params=None, method='GET'):
        with requests.Session() as s:
            p = self.authenticate_session(s)
            if p.status_code == 200:
                url = self.base_url + url
                # An authorised request.
                if method == "GET":
                    r = s.get(url)
                elif method == "POST":
                    r = s.post(url, params=params)
                elif method == "PUT":
                    r = s.put(url)
                elif method == "DELETE":
                    r = s.delete(url)

                if r.status_code == 204:
                    return True
                else:
                    return r.text.encode('utf-8').strip()

    #Set a media as a favorite
    def user(self):
        url = "/api/beta/user/"
        return self.make_request(url, method='GET')

    #Set a media as a favorite
    def favorite(self, media_id):
        url = "/api/beta/user/artworks/favorited/" + media_id
        return self.make_request(url, method='PUT')

    #Remove a media as a favorite
    def unfavorite(self, media_id):
        url = "/api/beta/user/artworks/favorited/" + media_id
        return self.make_request(url, method='DELETE')

    #Display a piece of media
    def display(self, media_id):
        url = "/api/beta/user/artworks/displayed/" + media_id
        return self.make_request(url, method='PUT')

    def favorites(self):
        url = "/api/beta/user/artworks/favorited"
        favorites_json = json.loads(self.make_request(url, method='GET'))
        return favorites_json

    #Display a piece of media
    def display_random_favorite(self):
        favs = self.favorites()
        fav = random.choice(favs)
        media_id = str(fav['artwork']['id'])
        return self.display(media_id)

    #Set a url to be on the display
    def set_url(self, url, device_id):
        set_url = '%s/set_url' % self.base_url
        with requests.Session() as s:
            p = self.authenticate_session(s)
            if p.status_code == 200:
                eo_sign = s.get(set_url)
                authenticity_token = self.authenticity_token(eo_sign.text)
                params = {
                  "custom_url": url,
                  "authenticity_token": authenticity_token,
                  "device_id": device_id
                }
                r = s.post(set_url, data=params)
                return r.status_code == 200
