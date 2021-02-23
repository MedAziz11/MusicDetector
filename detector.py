import os
from dotenv import load_dotenv
from typing import ByteString, List, Mapping

import requests
import pyaudio
import base64
from zlib import compress

load_dotenv()
class Detector(object):
    #class to detect music from a recorded sound

    def __init__(self) -> None:
        self.__KEY = os.environ.get('KEY')
        self.__HOST = "shazam.p.rapidapi.com"
        self.__URL = "https://shazam.p.rapidapi.com/"


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
            return{'error': 'Cant find lyrics...'}

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
            return {'error': "Sorry cant find the song..."}


    
    def runRecord(self):
        chunk = 512 # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 2

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 5 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')


        
        encoded_string =compress(encoded_string)
        return encoded_string 
        



    def detectSong(self, frames:bytes):
        endPoint = "songs/detect"
        payload = frames
        resp = requests.request(
            "POST",
            self.__URL+endPoint,
            data = payload, 
            headers = {'content-type': "application/xml" ,**self.__getHeaders()},
        )

        return resp.text


        

if __name__ == "__main__":
    d = Detector()

        # try :
        #     for song in d.searchSong("Godzilla"):
        #         print(f"{song['key']} : {song['title']} By {song['singer']}")

        #         print(d.getSongLyrics(song['key']))
        #         break

        # except: 
        #     pass

    #print(d.detectSong(d.runRecord()))