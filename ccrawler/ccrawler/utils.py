# utils.py
from http.cookies import SimpleCookie


def cookie_parse():
    cookie_string = ''
    # enter your cookies in the cookie string variable
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, value in cookie.items():
        cookies[key] = value.value

    return cookies