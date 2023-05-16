import ffmpeg

def get_video(file_path):
    try:
        return ffmpeg.input(file_path)
    except Exception as e:
        print("Couldn't get video.")
        print(e)

def convert_video_to_audio(video_path, output_path):
    print("Converting video to audio.")

    try:
        video = get_video(video_path)
        video.output(output_path, acodec="pcm_s16le", ac=1, ar="16k").run(quiet=True, overwrite_output=True)
    except Exception as e:
        print("Couldn't convert video to audio.")
        print(e)

    print("Video converted to audio.")

def create_video_with_subtitles(video_path, subtitles_path, output_path):
    print("Creating video with subtitles.")

    try:
        video = get_video(video_path)

        ffmpeg.concat(
            video.filter('subtitles', subtitles_path, force_style="OutlineColour=&H40000000,BorderStyle=3"), video.audio, v=1, a=1
        ).output(output_path).run(quiet=True, overwrite_output=True)
    except Exception as e:
        print("Couldn't create video with subtitles.")
        print(e)
    
    print("Video with subtitles created.")
