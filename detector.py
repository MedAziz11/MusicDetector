import os
from dotenv import load_dotenv
from typing import ByteString

import requests

load_dotenv()
class Detector(object):
    #class to detect music from a recorded sound


    def __init__(self) -> None:
        self.__KEY = os.environ.get('KEY')
        self.__HOST = "shazam.p.rapidapi.com"
        self.__URL = "https://shazam.p.rapidapi.com/"

    def runRecord(self)-> ByteString:
        pass

    def __getHeaders(self)->dict:
        headers = {
            'x-rapidapi-key': self.__KEY,
            'x-rapidapi-host': self.__HOST,
        }

        return headers

    def getSongDetails(self, song: str):
        endPoint = "songs/get-details"
        query = {"key": song, "locate": "en-US"}
        resp = requests.request(
            "GET", 
            self.__URL+endPoint,
            headers = self.__getHeaders(),
            params = query 
        )
        return resp.text

    def searchSong(self, song:str, limit = 5):
        endPoint = "search"
        query = {"term": song, "locate": "en-US", "offset":"0","limit":limit}
        resp = requests.request(
            "GET",
            self.__URL+endPoint,
            headers = self.__getHeaders(),
            params = query
        )

        return resp.text


d = Detector()
#print(d.getSongDetails('40333609'))
print(d.searchSong('clouds NF'))
