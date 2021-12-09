from uuid import uuid4
from urllib import parse


def generate_id(length:int=10):
    return int(str(uuid4().int)[:length])





def querystring_to_dict(url:str):
    if 'http' not in url and '?' not in url:
        url = '?'+url.strip()
    parse.urlsplit(url)
    parse.parse_qs(parse.urlsplit(url).query)
    return dict(parse.parse_qsl(parse.urlsplit(url).query))
