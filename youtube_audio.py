import http.client
import urllib.parse
import urllib.request
import re
import youtube_dl
import subprocess
import os
import sounddevice as sd
import soundfile as sf
import sys


class AudioClient:
    def __init__(self):
        self.audio_in = sd.default.device[0]
        self.audio_out = sd.default.device[1]

    @staticmethod
    def search(query):
        h1 = http.client.HTTPSConnection("www.youtube.com")
        try:
            h1.request("GET", "/results?search_query=" + urllib.parse.quote_plus(query))
        except Exception as e:
            print(e)
        response = h1.getresponse()
        return response.read()

    def get_video_id(self, query):
        html = self.search(query)
        match = re.search(r"href=\"/watch[^\"]+", str(html))
        return match.group(0)[15:]

    @staticmethod
    def get_download_link(vid_id):
        sys.stdout = open(os.devnull, 'w')
        ytd = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
        with ytd:
            result = ytd.extract_info("https://www.youtube.com/watch?v=" + vid_id, download=False)
            formats = result['formats']
            sys.stdout = sys.__stdout__
            return [x for x in formats if x['format_id'] == '139'][0]['url']

    def download_video(self, vid_id, file_name="audio"):
        url = self.get_download_link(vid_id)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        with open(file_name + ".mp3", "bw+") as file:
            file.write(data)
        file.close()

    @staticmethod
    def convert_to_wav(in_file="audio", out_file="audio", cleanup=True):
        cmd = "ffmpeg -i %s.mp3 %s.wav -loglevel quiet" % (in_file, out_file)
        subprocess.call(cmd.split(" "))
        if cleanup:
            os.remove("audio.mp3")

    def play_audio(self, file, cleanup=True):
        self.convert_to_wav(in_file=file, cleanup=cleanup)
        data, fs = sf.read("audio.wav", dtype='float32')
        sd.default.device = [self.audio_in, self.audio_out]
        sd.play(data, fs)
        os.remove("audio.wav")

    @staticmethod
    def stop_audio():
        sd.stop()

    @staticmethod
    def query_audio_devices():
        return sd.query_devices()
