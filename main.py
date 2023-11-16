from urllib.request import urlopen
import requests

def yandex_link(url):
    clickr_a = urlopen('https://clck.ru/--?url=' + url)
    clickr = clickr_a.read()
    clickr_clear = clickr.decode("utf-8")
    return clickr_clear

def tinyurl_link(url):
  base_url = 'http://tinyurl.com/api-create.php?url='
  response = requests.get(base_url+url)
  return response.text

def isgd_link(url):
    base_url = 'https://is.gd/create.php?format=simple&url='
    response = requests.get(base_url + url)
    return response.text
