import logging
import bleach
from bs4 import UnicodeDammit

def sanitize(text): 
    return bleach.clean(text, strip=True)

# def remove_newlines(text):
#     return u' '.join(text.splitlines())

def unicodify(text):
    try:
        return UnicodeDammit(text).unicode_markup
    except (ValueError, TypeError):
        logging.info('bad user input {0}'.format(text))
        return u''

def preprocess(text):
    sanitized = sanitize(text)
    unicodified = unicodify(sanitized)
    return unicodified.splitlines()

