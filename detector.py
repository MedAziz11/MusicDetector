import os
from dotenv import load_dotenv
from typing import ByteString, List, Mapping

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

    def __getHeaders(self)-> dict:
        headers = {
            'x-rapidapi-key': self.__KEY,
            'x-rapidapi-host': self.__HOST,
        }

        return headers

    def getSongLyrics(self, key: str)-> List:
        endPoint = "songs/get-details"
        query = {"key": key, "locate": "en-US"}
        resp = requests.request(
            "GET", 
            self.__URL+endPoint,
            headers = self.__getHeaders(),
            params = query 
        )
        try:         
            return resp.json()['sections'][1]['text']
        except KeyError:
            print('Cant find lyrics...')

    def searchSong(self, song:str, limit = 7)->Mapping:
        #returns a Map of dicts {title, key, singer, img}
        
        endPoint = "search"
        query = {"term": song, "locate": "en-US", "offset":"0","limit":limit}
        resp = requests.request(
            "GET",
            self.__URL+endPoint,
            headers = self.__getHeaders(),
            params = query
        )

        json_resp = resp.json()

        #cleaning data
        try : 
            data =  map(lambda track:{'title': track['track']["title"],'key': track['track']["key"], 'singer': track['track']["subtitle"], 'img': track['track']["share"]["image"]} , json_resp["tracks"]["hits"])
            return data
        except KeyError:
            print("Sorry cant find the song...")
        

        

if __name__ == "__main__":
    d = Detector()

    try :
    
        for song in d.searchSong("Godzilla"):
            print(f"{song['key']} : {song['title']} By {song['singer']}")

            print(d.getSongLyrics(song['key']))
            break

    except: 
        pass


