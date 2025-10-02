from .transcriber import Transcriber
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Automatically subtitle any video spoken in any language to a language of your choice."
    )
    parser.add_argument("video_file", help="Path to video file.")
    parser.add_argument("-o", "--output_video_file", help="Path to output video file.")
    parser.add_argument(
        "-srt", "--output_subtitle_file", help="Path to output SRT file.", default="output.srt"
    )
    parser.add_argument(
        "-srclang", "--source_language", help="Source language for translation.", default=None
    )
    parser.add_argument(
        "-tgtlang", "--target_language", help="Target language for translation.", default=None
    )
    parser.add_argument("-captype", "--captioning_model_type", help="Model type.", default="base")
    parser.add_argument(
        "-langtype", "--language_model_type", help="Language model type.", default="base"
    )
    parser.add_argument("-mdir", "--model_dir", help="Path to model directory.", default=None)
    args = parser.parse_args()
    Transcriber.transcribe(
        args.video_file,
        args.output_video_file,
        args.output_subtitle_file,
        args.source_language,
        args.target_language,
        args.captioning_model_type,
        args.language_model_type,
        args.model_dir,
    )
