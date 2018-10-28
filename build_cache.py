import os
import logging
import json
from collections import defaultdict

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(BASE_DIR, 'textfiles')

def append_word_if_eligible(word, words_by_len):
    word = word.strip("\n").strip()
    if not word.endswith("'s"): # crude handling of English possessives
        length = str(len(word)) # because JSON does not allow int keys
        begins_with = word[0]
        words_by_len[length][begins_with].append(word)

def process_filename(dirname, filename):
    words_by_len = defaultdict(lambda: defaultdict(list))
    fullpath = os.path.join(TEXT_DIR, dirname, filename)
    with open(fullpath, encoding=dirname) as f:
        for word in f.readlines():
            append_word_if_eligible(word, words_by_len)
    return words_by_len

def build_cache():
    datastore = {}
    for dirname in [item for item in os.listdir(TEXT_DIR) if '.' not in item]:
        raw_filenames = os.listdir(os.path.join(TEXT_DIR, dirname))
        eligible_filenames = [f for f in raw_filenames if not f.startswith('.')]
        for language in eligible_filenames:
            words_by_len = process_filename(dirname, language)
            datastore[language] = words_by_len
    return datastore

def get_cache():
    try:
        with open(os.path.join(TEXT_DIR, 'datastore.json'), 'r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print('Please wait: building language cache...')
        return build_cache()

if __name__ == "__main__":
    cache = build_cache()
    with open(os.path.join(TEXT_DIR, 'datastore.json'), 'w') as f:
        f.write(json.dumps(cache))

