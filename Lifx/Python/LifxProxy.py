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
        print(uri)
        response = requests.get(uri, headers = self._headers)

        result = LifxProxyResult(999, {})
        if response:
            result = LifxProxyResult(response.status_code, json.loads(response.text))

        return result

    def ToggleLight(self, value, selectorType = 'all'):
        if not selectorType == 'all':
            if value == None:
                raise TypeError('[value] cannot be None.')
        
        typeSwitch = {
            'id': 'id:%s' % value,
            'label': 'label:%s' % value,
            'group_id': 'group_id:%s' % value,
            'group': 'group:%s' % value,
            'location_id': 'location_id:%s' % value,
            'location': 'location:%s' % value,
            'scene_id': 'scene_id:%s' % value
        }

        #If nothing just for fun Toggle ALL lights
        selector = '%s/toggle' % typeSwitch.get(selectorType, 'all')   

        uri = '%s%s' % (self._baseUri, selector)
        print(uri)
        response = requests.post(uri, headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))
        

    def ToggleAllLights(self):
        selector = 'all/toggle';

        uri = '%s%s' % (self._baseUri, selector)
        response = requests.post(uri, headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))
        

    def AllLightsOff(self):
        selector = 'all/state'

        payload = {
            'power': 'off'
        }

        uri = '%s%s' % (self._baseUri, selector)
        response = requests.put(uri, data = payload,  headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))      

    def AllLightsOn(self):
        selector = 'all/state';

        payload = {
            'power': 'on'
        }

        uri = '%s%s' % (self._baseUri, selector)
        response = requests.put(uri, data = payload,  headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))

    #Change the State of the lightbulb
    #Control
    #    -Color (string) : name, hex 
    #    -Brightness (double): double value defaults to 100 (1.0)%
    def ChangeAllLightSettings(self, colorValue, brightness = 1.0):
        selector = 'all/state';

        payload = {
            'color': colorValue,
            'brightness': brightness
        }

        uri = '%s%s' % (self._baseUri, selector)
        response = requests.put(uri, data = payload,  headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))

    def ChangeLightColor(self, color, selectorValue, selectorType = 'all'):
        if not selectorType == 'all':
            if selectorValue == None:
                raise TypeError('[value] cannot be None.')
        
        typeSwitch = {
            'id': 'id:%s' % selectorValue,
            'label': 'label:%s' % selectorValue,
            'group_id': 'group_id:%s' % selectorValue,
            'group': 'group:%s' % selectorValue,
            'location_id': 'location_id:%s' % selectorValue,
            'location': 'location:%s' % selectorValue,
            'scene_id': 'scene_id:%s' % selectorValue
        }
        
        selector = '%s/state' % typeSwitch.get(selectorType)

        payload = {
            'color': color
        }

        uri = '%s%s' % (self._baseUri, selector)
        response =  requests.put(uri, data = payload, headers = self._headers)

        return LifxProxyResult(response.status_code, json.loads(response.text))

    def GetScenes(self):
        selector = 'scenes'

        uri = '%s%s' % (self._baseUri.split('lights')[0], selector)

        response = requests.get(uri, headers = self._headers)

        return LifxProxyResult(response.status_code, response.text)

#Lifx Proxy Result
class LifxProxyResult():

    def __init__(self, code, jsonResult):
        if not type(code) is int:
            raise TypeError('responseCode must be a integer')

        self.responseCode = code
        self.result = jsonResult

#class Color
class LifxColor():

    def __init__(self, saturation, kelvin, hue):
        self.saturation = saturation
        self.kelvin = kelvin
        self.hue = hue
