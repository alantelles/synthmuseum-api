import requests

URL = 'https://www.synthmuseum.com'

def request_index_page():
    url = URL
    res = requests.get(url)
    return res.content.decode()

def request_company_page(company):
    url = f'{URL}/{company}/index.html'
    res = requests.get(url)
    return res.content.decode()