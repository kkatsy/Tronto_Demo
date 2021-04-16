import requests
from bs4 import BeautifulSoup

blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
    'a',
    'style',
    'title',
    'link',
    'span',
    'body',
    'nav',
]

whitelist = ['div', 'p']


def get_context(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''

    prev = ''
    prev_content = ''

    for t in text:
        if t.parent.name == 'a' and prev in ['p', 'div']:
            prev += ' a'
            prev_content = t
            prev_prev_t = prev_t

        # if t.parent.name not in blacklist:
        if t.parent.name in whitelist:
            if len(prev.split()) == 2 and prev.split()[-1] == "a" and t.parent.name == prev.split()[0] and len(prev_prev_t.strip()) > 0:
                output += '{} '.format(prev_content.strip())

            prev = t.parent.name
            prev_content = ""

            output += '{} '.format(t.strip())

        if t.parent.name != 'a':
            prev = t.parent.name
            prev_content = ''

        prev_t = t

    return output
