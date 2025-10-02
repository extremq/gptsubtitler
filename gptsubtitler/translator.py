from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import os


class Translator(object):
    model = None
    tokenizer = None
    model_type = None
    model_dir = None
    AVAILABLE_MODELS = ["base", "large"]

    @staticmethod
    def create_model_and_tokenizer():
        # Set model directory
        if Translator.model_dir is not None:
            if os.environ.get("HF_HOME") is None:
                raise Exception(
                    "HF_HOME environment variable not set! Please set HF_HOME environment variable! Otherwise, run without model_dir parameter."
                )

        if Translator.model is None:
            try:
                if Translator.model_type == "base":
                    Translator.model = M2M100ForConditionalGeneration.from_pretrained(
                        "facebook/m2m100_418M"
                    )
                elif Translator.model_type == "large":
                    Translator.model = M2M100ForConditionalGeneration.from_pretrained(
                        "facebook/m2m100_1.2B"
                    )
            except Exception as e:
                print("Couldn't load model.")
                print(e)

        if Translator.tokenizer is None:
            try:
                if Translator.model_type == "base":
                    Translator.tokenizer = M2M100Tokenizer.from_pretrained(
                        "facebook/m2m100_418M"
                    )
                elif Translator.model_type == "large":
                    Translator.tokenizer = M2M100Tokenizer.from_pretrained(
                        "facebook/m2m100_1.2B"
                    )
            except Exception as e:
                print("Couldn't load tokenizer.")
                print(e)

    @staticmethod
    def translate(
        text,
        source_language="en",
        target_language="ro",
        model_type="base",
        model_dir=None,
    ):
        """Translate text.

        Args:
            text (str): Text to translate.

            source_language (str, optional): Source language. Defaults to "en".

            target_language (str, optional): Target language. Defaults to "ro".

            model_type (str, optional): Model type. Defaults to "base".
        Returns:
            str: Translated text.
        """
        if model_type not in Translator.AVAILABLE_MODELS:
            print(
                f"Invalid 'model_type'. Using base model. Available models: {Translator.AVAILABLE_MODELS}"
            )
            model_type = "base"

        # Set model directory
        Translator.model_dir = model_dir

        # Set model type
        Translator.model_type = model_type

        Translator.create_model_and_tokenizer()

        # Set source language for tokenizer
        Translator.tokenizer.src_lang = source_language

        # Try to encode text
        try:
            encoded_text = Translator.tokenizer(text, return_tensors="pt")
        except Exception as e:
            print("Couldn't encode text.")
            print(e)

        # Try to generate tokens
        try:
            generated_tokens = Translator.model.generate(
                **encoded_text,
                forced_bos_token_id=Translator.tokenizer.get_lang_id(target_language),
            )
        except Exception as e:
            print("Couldn't generate tokens. Maybe language is not supported.")
            print(e)

        target_text = None

        # Try to decode tokens
        try:
            target_text = Translator.tokenizer.batch_decode(
                generated_tokens, skip_special_tokens=True
            )
        except Exception as e:
            print("Couldn't decode tokens.")
            print(e)

        # Return translated text
        if target_text is not None:
            return target_text[0]
        else:
            return target_text
