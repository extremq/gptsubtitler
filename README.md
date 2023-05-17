# Subtitler
Automatically subtitle any video spoken in any language to a language of your choice.

Models used:
- [OpenAI whisper](https://openai.com/research/whisper) - for text-to-audio
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

You only need to specify the language you want the subtitles to be in, the program will handle the rest of the work.
```py
from gptsubtitler import Transcriber

# I strongly recommend using the "medium" model_type.
Transcriber.transcribe("soldier.mp4", target_language="ro", model_type="medium", language_model_type="base")

# If you want to use the gpu, add device="cuda"
# Transcriber.transcribe("soldier.mp4", target_language="ro", model_type="medium", language_model_type="base", device="cuda") 
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
Device (if you have a gpu and have installed [pytorch](https://pytorch.org/get-started/locally/), use "cuda"):
- cpu - default
- cuda

Available options for `model_type` (the audio to text model):
- tiny
- base - default
- small
- medium
- large

Available options for `language_model_type` (the language translator model):
- base - default
- large
