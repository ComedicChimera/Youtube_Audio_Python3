import http.client
import urllib.parse
import urllib.request
import re

# mandatory installs
import pafy

# VLC must be installed in order for this to work
import vlc


# AudioClient
# Primary Class Provided by YoutubeAudio
class AudioClient:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.audio_out = None
        self.is_playing = False
        self.update_audio_out = False

    # execute http request to find youtube page containing results
    # used to find response page
    @staticmethod
    def search(query):
        h1 = http.client.HTTPSConnection("www.youtube.com")
        try:
            h1.request("GET", "/results?search_query=" + urllib.parse.quote_plus(query))
        except Exception as e:
            print(e)
        response = h1.getresponse()
        return response.read()

    # main search function
    # takes in query and derives video id of first file
    def get_video_id(self, query):
        html = self.search(query)
        match = re.search(r"href=\"/watch[^\"]+", str(html))
        return match.group(0)[15:]

    # get video data
    @ staticmethod
    def get_video_data(vid_id):
        return pafy.new("https://www.youtube.com/watch?v=" + vid_id)

    # obtains the best audio (mp3) download link from a specific video id
    @staticmethod
    def get_download_link(vid_id):
        video = pafy.new("https://www.youtube.com/watch?v=" + vid_id)
        return video.getbestaudio().url

    # used to download a file from the video id
    def download_video(self, vid_id, file_name="audio"):
        url = self.get_download_link(vid_id)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        with open(file_name + ".mp3", "bw+") as file:
            file.write(data)
        file.close()

    # play back audio either from file path or from url
    def play_audio(self, path):
        self.player.set_mrl(path)
        self.is_playing = True
        if self.update_audio_out and self.audio_out:
            self.player.audio_output_device_set(None, self.audio_out)
            self.update_audio_out = False
        self.player.play()

    # set audio output
    def set_audio_out(self, out):
        if self.audio_out != out:
            self.player.audio_output_device_set(None, out)
            self.audio_out = out

    # stop audio playback - will fail if audio is not currently playing
    def stop_audio(self):
        if self.is_playing:
            self.is_playing = False
            self.player.stop()
            self.update_audio_out = True
            self.player = vlc.MediaPlayer()
        else:
            raise YoutubeAudioError("Unable to stop MediaPlayer not playing audio.")

    # used to pause and unpause the audio stream
    # False is playing, True is paused
    def set_pause_state(self, state):
        if self.is_playing:
            self.player.set_pause(int(state))
        else:
            raise YoutubeAudioError("Unable to pause/resume MediaPlayer not playing audio.")

    # adjustable volume property
    # can be set or fetched depending on use case
    def volume(self, * value):
        if value:
            self.player.audio_set_volume(value[0])
        else:
            return self.player.audio_get_volume()

    # returns a list of all available audio devices
    # keys are ids, values are descriptions
    def query_output_devices(self):
        devices = {}
        mods = self.player.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                if mod.device.decode('ascii') != '':
                    devices[mod.device.decode('ascii')] = mod.description.decode('ascii')
                mod = mod.next
        vlc.libvlc_audio_output_device_list_release(mods)
        return devices


# class for errors when using API
class YoutubeAudioError(Exception):
    pass
