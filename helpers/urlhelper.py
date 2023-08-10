import urllib
from urllib.error import HTTPError
import validators
from validators import ValidationFailure
import requests

#Checks if the path is formatted as a URL
def is_path_url(url_string) -> bool:
    result = validators.url(url_string)
    if isinstance(result, ValidationFailure):
        return False

    return result
    
#Sees if the URL leads to an actual link
def url_ok(url):
    r = requests.head(url)
    print("Is URL OK")
    print(r.status_code)
    return r.status_code != 404