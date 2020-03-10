import requests,re,traceback
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                   'Accept' : '*/*'}
        r = requests.get(url,timeout=30,headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def getSoupObj(url):
    try:
        html = getHTMLText(url)
        soup = BeautifulSoup(html,'html.parser')
        return soup
    except:
        print('\nError: failed to get the Soup object')
        return None

def get_download_links(url):
    soup = getSoupObj(url)
    try:
        contents = soup('div',{'id':'content'})
        links = contents[0]('center')[0]('a')[0]['href']
        return links
    except Exception:
        traceback.print_exc()
        return ''

def get_page_data(url):
    print(url)
    soup = getSoupObj(url)
    is_end = False
    result = {}
    try:
        contents = soup('div',{'id':'content'})
        articles = contents[0].find_all('article')
        for article in articles:
            title = article('h1', {'class': 'entry-title'})[0]
            name = title('a')[0].text
            href = title('a')[0]['href']

            download_links = get_download_links(href)
            result[name] = download_links
    except Exception:
        traceback.print_exc()
        is_end = True
        pass

    return is_end, result

def getInfo(request_url, cur_page):
    while True:
        search_url = request_url + "&paged=" + str(cur_page)
        is_end, data_map = get_page_data(search_url)
        if is_end:
            break
        else:
            for name in data_map.keys():
                print(name)
            for url in data_map.values():
                print(url)
        input("点击查找下一页")
        cur_page += 1

if __name__=="__main__":
    url = ''
    start_page = 1
    getInfo(url, start_page)
