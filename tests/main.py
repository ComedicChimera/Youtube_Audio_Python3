from youtube_audio import AudioClient

while True:
    query = input("Enter a song name:\n")
    client = AudioClient()
    if query == "STOP":
        client.stop_audio()
        continue
    video_id = client.get_video_id(query)
    client.download_video(video_id)
    client.play_audio("audio")
