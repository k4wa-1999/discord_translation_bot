from googletrans import Translator


def translation(translation_lang,translation_message):
    translator = Translator()
    translated = translator.translate(translation_message, dest=translation_lang,)
    translation_text = translated.text
    translation_text = translation_text.replace( '\n' , '' )
    return translation_text

