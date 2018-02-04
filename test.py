from youtube_audio import AudioClient

while True:
    query = input("Enter a song name:\n")
    client = AudioClient()
    video_id = client.get_video_id(query)
    download_link = client.get_download_link(video_id)
    # print("Downloading")
    # client.download_video(video_id)
    # virtual audio things
    # client.audio_out = 7
    print("Playing\n")
    client.play_stream(download_link, output="CABLE Output")
    # client.play_audio("audio", False)
