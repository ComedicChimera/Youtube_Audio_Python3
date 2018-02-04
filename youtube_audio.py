import http.client
import urllib.parse
import urllib.request
import re
import subprocess
import os
import pafy


class AudioClient:
    def __init__(self):
        pass

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
        video = pafy.new("https://www.youtube.com/watch?v=" + vid_id)
        return video.getbestaudio().url

    def download_video(self, vid_id, file_name="audio"):
        url = self.get_download_link(vid_id)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        with open(file_name + ".mp3", "bw+") as file:
            file.write(data)
        file.close()

    @staticmethod
    def convert_to_wav(in_file, out_file, cleanup=False):
        cmd = "ffmpeg -i %s.mp3 %s.wav -loglevel panic -hidebanner" % (in_file, out_file)
        subprocess.call(cmd.split(" "))
        if cleanup:
            os.remove("audio.mp3")

    @staticmethod
    def play_file(file, volume=50, cleanup=False):
        cmd = "ffplay -loglevel panic -nodisp -volume %s -i %s" % (volume, file)
        subprocess.call(cmd.split(" "))
        if cleanup:
            os.remove(file)

    @staticmethod
    def play_stream(url, volume=50, output=None):
        # add customizable output
        cmd = "ffplay -loglevel panic -nodisp -volume %s -i %s" % (volume, url)
        subprocess.call(cmd.split(" "))

    @staticmethod
    def stop():
        subprocess.call(['ffplay', 'q'])

    @staticmethod
    def pause():
        subprocess.call(['ffplay', 'p'])
