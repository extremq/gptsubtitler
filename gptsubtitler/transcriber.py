import whisper
from pywhispercpp.model import Model
from .video_utils import convert_video_to_audio, create_video_with_subtitles
from .translator import Translator
import os


class Transcriber(object):
    model = None
    captioning_model_type = None
    target_language = None
    source_language = None
    language_model_type = None
    model_dir = None
    AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large"]

    @staticmethod
    def create_model():
        if Transcriber.model is None:
            # Choose number of threads
            threads = os.cpu_count()
            if threads is None:
                threads = 1
            else:
                threads = threads // 2

            try:
                # Set model directory if specified
                if Transcriber.model_dir is not None:
                    if os.environ.get("HF_HOME") is None:
                        raise Exception(
                            "HF_HOME environment variable not set! Please set HF_HOME environment variable! Otherwise, run without model_dir parameter."
                        )
                    else:
                        Transcriber.model = Model(Transcriber.captioning_model_type, n_threads=threads, models_dir=Transcriber.model_dir)
                else:
                    Transcriber.model = Model(Transcriber.captioning_model_type, n_threads=threads)
            except Exception as e:
                print("Couldn't load model.")
                print(e)

    @staticmethod
    def transcribe(
        video_file,
        output_video_file=None,
        output_subtitle_file="output.srt",
        source_language=None,
        target_language=None,
        captioning_model_type="base",
        language_model_type="base",
        model_dir=None
    ):
        """Transcribe video file and generate SRT file.

        Args:
            video_file (str): Path to video file.

            output_video_file (str, optional): Path to output video file. Defaults to None.

            output_subtitle_file (str, optional): Path to output SRT file. Defaults to "output.srt".

            source_language (str, optional): Source language for translation. Defaults to None.

            target_language (str, optional): Target language for translation. Defaults to None.

            captioning_model_type (str, optional): Model type. Defaults to "base".

            language_model_type (str, optional): Language model type. Defaults to "base".

            model_dir (str, optional): Path to model directory. Defaults to None.
        """
        if captioning_model_type not in Transcriber.AVAILABLE_MODELS:
            print(
                f"Invalid 'captioning_model_type'. Using base model. Available models: {Transcriber.AVAILABLE_MODELS}"
            )
            captioning_model_type = "base"

        if source_language is None:
            print("Source language not specified. Using English.")
            source_language = "en"

        # Set target language
        Transcriber.target_language = target_language

        # Set source language
        Transcriber.source_language = source_language

        # Set language model type
        Transcriber.language_model_type = language_model_type

        # Set model type
        Transcriber.captioning_model_type = captioning_model_type

        # Set model directory
        Transcriber.model_dir = model_dir

        # Create model
        Transcriber.create_model()

        if output_video_file is None:
            # Set output video file
            dot = video_file.rfind(".")
            output_video_file = video_file[:dot] + "_subtitled" + video_file[dot:]

        # Try to transcribe audio
        transcript = None
        try:
            print("Converting video to audio.")
            convert_video_to_audio(video_file, "temporary_audio.wav")
            print("Video converted to audio.")

            print("Captioning audio.")
            transcript = Transcriber.model.transcribe(
                "temporary_audio.wav", language=Transcriber.source_language, speed_up=True, print_progress=False
            )
            print("Finished captioning.")

            os.remove("temporary_audio.wav")
        except Exception as e:
            print("Couldn't transcribe audio.")
            print(e)

        # Add .srt extension if not present
        if not output_subtitle_file.endswith(".srt"):
            output_subtitle_file += ".srt"

        # Try to generate SRT file
        srt_content = Transcriber.generate_srt_file(transcript, supress_output=True)

        # Checkpoint SRT file
        with open("checkpoint_" + output_subtitle_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        try:
            print("Generating SRT file.")
            srt_content = Transcriber.generate_srt_file(transcript, supress_output=False, with_translation=True)
            print("SRT file generated.")
        except Exception as e:
            print("Couldn't generate SRT file.")
            print(e)

        # Write final SRT file
        with open(output_subtitle_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        # Create video with subtitles
        print("Creating video with subtitles.")
        create_video_with_subtitles(video_file, output_subtitle_file, output_video_file)
        print("Video with subtitles created.")

    @staticmethod
    def generate_srt_file(transcript, with_translation=False, supress_output=False):
        srt_content = ""
        if supress_output is False:
            print(f"Total lines: {len(transcript)}")
        for count, line in enumerate(transcript):
            # Add line number
            srt_content += str(count) + "\n"

            # Add timestamps
            srt_content += (
                Transcriber.format_seconds_to_srt_timestamp(line.t0)
                + " --> "
                + Transcriber.format_seconds_to_srt_timestamp(line.t1)
                + "\n"
            )

            # Add text
            text = line.text.strip()
            if with_translation is True and Transcriber.target_language is not None and Transcriber.target_language != Transcriber.source_language:
                # Translate text only if user wanted to translate text
                text = Translator.translate(
                    text,
                    source_language=Transcriber.source_language,
                    target_language=Transcriber.target_language,
                    model_type=Transcriber.language_model_type,
                    model_dir=Transcriber.model_dir,
                ).strip()

                if supress_output is False:
                    print(
                        f"- Line {count + 1} of {len(transcript)}: {line.text}\n --> {text}"
                    )
            else:
                if supress_output is False:
                    print(
                        f"- Line {count + 1} of {len(transcript)}: {line.text}"
                    )
            srt_content += text + "\n"

            srt_content += "\n"

        return srt_content

    @staticmethod
    def format_seconds_to_srt_timestamp(seconds):
        milliseconds = round(seconds * 10.0)

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        return f"{hours}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
