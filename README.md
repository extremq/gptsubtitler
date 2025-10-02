# Subtitler
Automatically subtitle any video spoken in any language to a language of your choice using AI.

Models used:
- [OpenAI whisper C++ port](https://github.com/ggerganov/whisper.cpp) - for audio-to-text
- [Facebook M2M10](https://huggingface.co/facebook/m2m100_418M) - for translation

Tools used:
- `ffmpeg`

**Please don't forget to star the repository if you find it useful or educational!**

Before:

https://github.com/extremq/subtitler/assets/45830561/49f6ecce-cfdc-4f1c-97eb-07a36ac841c9

After (in Romanian - `model_type=medium, language_model_type=base`):

https://github.com/extremq/subtitler/assets/45830561/20bc5169-0ce3-47cd-adb7-15d75daf27f4

# Setup
Install using `pip`.

```
pip install gptsubtitler
```

Install [`ffmpeg`](https://ffmpeg.org/):
```bash
# Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# MacOS
brew install ffmpeg

# Windows using Chocolatey https://chocolatey.org/
choco install ffmpeg
```

# Quick guide
Example usage for adding subtitles and translating them in Romanian:

Command line:
```bash
gptsubtitler soldier.mp4 --source_language en --target_language ro --captioning_model_type medium --language_model_type base
```

Or in Python
```py
from gptsubtitler import Transcriber

# I strongly recommend using the "medium" model_type.
Transcriber.transcribe("soldier.mp4", source_language="en", target_language="ro", captioning_model_type="medium", language_model_type="base")
```

You can also use the `Translator` class from `translator.py` if you just want to translate some text.

Example usage for translating from English to Romanian:
```py
from gptsubtitler import Translator

print(Translator.translate("Hi!", target_language="ro", source_language="en"))
```

If you have generated a `.srt` file and just want to add subtitles:
```py
from gptsubtitler import create_video_with_subtitles
create_video_with_subtitles("video.mp4", "output.srt", "video_subtitled.mp4")
```

# Options
```
Args:
    video_file (str): Path to video file.

    output_video_file (str, optional): Path to output video file. Defaults to video_file_subtitled.

    output_subtitle_file (str, optional): Path to output SRT file. Defaults to "output.srt".

    source_language (str, optional): Source language for translation. Defaults to en.

    target_language (str, optional): Target language for translation. Defaults to None.

    captioning_model_type (str, optional): Model type. Defaults to "base".

    language_model_type (str, optional): Language model type. Defaults to "base".

    model_dir (str, optional): Path to model directory. Defaults to None.
```

Available options for `captioning_model_type` (the audio to text model):
- tiny
- base - default
- small
- medium
- large

Available options for `language_model_type` (the language translator model):
- base - default
- large
