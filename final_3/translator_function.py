from googletrans import Translator, LANGUAGES

# Initialize the translator
translator = Translator()

def get_language_code(language_name):
    """Return the language code for a given language name."""
    language_mapping = {name.lower(): code for code, name in LANGUAGES.items()}
    return language_mapping.get(language_name.lower(), None)

def translate_to_english(text, from_language):
    """Translate the spoken text to English."""
    return translator.translate(text, src=from_language, dest='en').text

def translate_from_english(text, to_language):
    """Translate the text from English to the target language."""
    return translator.translate(text, src='en', dest=to_language).text
