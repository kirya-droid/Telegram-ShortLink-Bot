from urllib.request import urlopen



def fastlink(url):
    clickr_a = urlopen('https://clck.ru/--?url=' + url)
    clickr = clickr_a.read()
    clickr_clear = clickr.decode("utf-8")
    return clickr_clear


