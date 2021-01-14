import requests
import json
import datetime
import sys

class AssetLoader:
    """ Used to store HTTP session """
    __http_session = ''
    """ Shard context """
    _json_assets = ''
    __assets = {}

    _username = ''
    _password = ''
    _endpoint = ''

    def __init__(self, shard_endpoint, username, password):
        self._username = username
        self._password = password
        self._endpoint = shard_endpoint

        """ Build HTTP session """
        auth_http_status = self.__auth_with_shard()
        if auth_http_status == 200:
            self.__load_assets()
        else:
            print("An error occured while authenticating. HTTP Status " + str(auth_http_status))

    def __auth_with_shard(self):
        """ POST login/password and build session """
        self.__http_session = requests.Session()
        r = self.__http_session.post(self._endpoint + '/auth/signIn', data={'login':self._username, 'password':self._password})
        print("__auth_with_shard:: " + str(r.status_code))

        return r.status_code

    def get_label(self, label_code):
        return self.__assets['labels'][label_code]

    def __load_assets(self):
        """ GET assets """
        r = self.__http_session.get(self._endpoint + '/label')
        self._json_assets = r.json()

        self.__assets['labels'] = {}
        labels = self._json_assets

        for lbl in labels:
            self.__assets['labels'][lbl['name']] = lbl['zpl']

        print("__load_assets :: Labels (" + str(len(self.__assets['labels'])) + ") loaded.")