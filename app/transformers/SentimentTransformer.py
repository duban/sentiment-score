from polyglot.text import Text
from polyglot.detect import Detector
from collections import Counter
import pandas as pd
import json

def polarity(text, language):
    polyglot_languages = ["en", "vi", "id"]
    language_code = language if language in polyglot_languages else Detector(text, quiet=True).language.code
    poly_text = Text(text, hint_language_code=language_code)

    pos, neg, neu = 0, 0, 0

    for word in poly_text.words:
        if word.polarity == -1:
            neg = neg + 1
        elif word.polarity == 1:
            pos = pos + 1
        else:
            neu = neu + 1

    res = {'txt': text,
           'pos': pos / (pos + neg + 0.0001),
           'neg': neg / (pos + neg + 0.0001),
           'neu': neu / (len(poly_text.words) + 0.0001),
           'language_code': language_code}

    return res

def sentiment_process_v2(json_array):
    new_list = []
    for item in json_array:
        new = polarity(item['txt'], item['lang'])
        new_list.append({'id': item['id'], 'txt': item['txt'], 'language_code': new['language_code'],
                         'neg': new['neg'], 'neu': new['neu'], 'pos': new['pos']})

    df = pd.DataFrame(new_list)
    dt = df.to_dict('records')
    ds = {"result": dt}
    # dj = json.dumps(ds, sort_keys=True, indent=4, ensure_ascii=False)

    return new_list