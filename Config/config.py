import json


class Config:
    def GetConfig(self, type):
        with open('config.json') as j:
            data = json.load(j)
            return data[type]
