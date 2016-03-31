import sys
import logging
import requests
import json

#Class for communicating with the Lifx api
#You must have created a cloud account at https://cloud.lifx.com/
#Current api is 'https://api.lifx.com/v1/lights/' but is a parmeter if this should change
class LifxProxy():

    def __init__(self, baseUri, token, loggingStream = sys.stderr, debuggingLevel = logging.DEBUG, loggingFile = ''):
        if not type(baseUri) is str:
            raise TypeError('baseUri must be of type string')
        
        if not type(token) is str:
            raise TypeError('token must be of type string')

        if baseUri.strip():
            baseUri = 'https://api.lifx.com/v1/lights/'

        self._baseUri = baseUri
        self._headers = {
            'Authorization': 'Bearer %s' % token
        }

        if not loggingFile.strip():
            logging.basicConfig(filename = loggingFile, level = debuggingLevel)
        else:
            logging.basicConfig(stream = loggingStream, level = debuggingLevel)

    def GetAllLifxs(self):
        selector = 'all';

        uri = '%s%s' % (self._baseUri, selector)

        response = requests.get(uri, headers = self._headers)

        result = LifxProxyResult(999, {})
        if response:
            result = LifxProxyResult(response.status_code, json.loads(response.text))

        return result

    def ToggleAllLights(self):
        selector = 'all/toggle';

        uri = '%s%s' % (self._baseUri, selector)

        response = requests.get(uri, headers = self._headers)

        return response
        

    def AllLightsOff(self):
        selector = 'all/state'

        payload = {
            'power': 'off'
        }

        uri = '%s%s' % (self._baseUri, selector)
        response = requests.get(uri,  data = payload, headers = self._headers)

        return json.loads(response.text)      

    def AllLightsOn(self):
        selector = 'all/state';

        payload = {
            'power': 'on'
        }

        uri = '%s%s' % (self._baseUri, selector)
        
        response = requests.get(uri,  data = payload, headers = self._headers)

        return json.loads(response.text)


class LifxProxyResult():

    def __init__(self, code, jsonResult):
        if not type(code) is int:
            raise TypeError('responseCode must be a integer')

        self.responseCode = code
        self.result = jsonResult

    
