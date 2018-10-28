import json
from operator import itemgetter
from fuzzywuzzy import fuzz
from build_cache import get_cache

cache = get_cache()

TOP_X = 20

def get_languages():
    return sorted(list(cache.keys()))

def select_best(token, targets):
    return sorted([(target, fuzz.ratio(token, target)) for target in targets], key=itemgetter(1), reverse=True)

def get_targets_for_token(token, language):
    starting_letter = token[0].lower()
    token_length = str(len(token)) # because JSON does not allow int keys
    from_lang_by_length = cache.get(language, {}).get(token_length, {})
    targets = from_lang_by_length.get(starting_letter)
    if not targets:
        targets = [item for sublist in from_lang_by_length.values() for item in sublist] # fall back to all items of same length starting with whatever
    return targets

def select_top_n_targets(targets, token, n=TOP_X, remove_distance_vals=True):
    if targets: #ta
        if len(targets) > 1:
            top_match, dist = targets[0][0], targets[0][1]
            if dist == 100 or top_match.lower() == token.lower():
                targets = targets[1: n+1]
        else:
            targets = targets[:n]
        if remove_distance_vals:
            targets = [target[0] for target in targets] # remove distance values
    return targets

def process_token(token, target_language):
    targets = get_targets_for_token(token, target_language)
    if targets:
        best = select_best(token, targets)
        return select_top_n_targets(best, token)
    return [token] # nothing found - return same

def get_tokens(phrase):
    return phrase.strip().split()

def zip_results(results):
    # [['Mike', 'Mieke'], ['Scharf', 'Scarfe']] --> ['Mike Scharf', 'Mieke Scarfe']
    return [" ".join(list(item)) for item in zip(*results)]

def process_phrase(phrase, target_language):
    return [process_token(token, target_language) for token in get_tokens(phrase)]

def xlangify_phrase(phrase, target_language):
    results = process_phrase(phrase, target_language)
    return zip_results(results)

def xlangify_lines(text, target_language):
    results = []
    for line in text:
        new_phrases = xlangify_phrase(line, target_language)
        if new_phrases:
            results.append(new_phrases[0])
    return results


