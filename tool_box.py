# -*- coding:UTF-8 -*-
import os
import json

class tool_box():

    def __init__(self):
        self.current_path = os.path.dirname(__file__)

    # create floder
    def mkdir(self, path):  
        path = path.strip()
        isExists = os.path.exists(path)

        if not isExists:
            os.makedirs(path)
            print('floder ' + path + ' is created successfully.')
        else:
            print('path ' + path + ' is already existed.')

    # get configuration information
    def get_config(self): 
        path = self.current_path + '/config.json'
        with open(path, 'r') as f:
            configfile = self.byteify(json.load(f))
        return configfile

    # as pyhon defaul load python to unicode, we need to encode josn as utf-8 string.
    def byteify(self, input, encoding='utf-8'): 
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode(encoding)
        else:
            return input
