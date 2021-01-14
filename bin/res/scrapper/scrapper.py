import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def try_request(url):
    try:
        return requests.get(url)
    except:
        try_request(url)

def scrap_goodreads_table(url):
    t1 = time.time()
    check = lambda x: x if x is not None else BeautifulSoup("<p>NONE</p>", features='lxml')
    dic = {'Title_URL': [], 'Title': [], 'Author': [], 'minirating': [], 'num_reviews': [], 'num_pages': [], 'awards': [], 'genres': [], 'series': [], 'year_published': [], 'places': []}
    for i in range(1, 11): # number of pages to scrap (100 positions per page)
        page = try_request(url + '?page=' + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')
        contents = [soup.findAll('a', class_='bookTitle'), soup.findAll('a', class_='authorName'), soup.findAll('span', class_='minirating')]
        dic['Title'] += [contents[0][j].get_text().strip() for j in range(100)]
        dic['Title_URL'] += ["https://www.goodreads.com" + contents[0][j]['href'] for j in range(100)]
        dic['Author'] += [contents[1][j].get_text() for j in range(100)]
        dic['minirating'] += [contents[2][j].get_text() for j in range(100)]
    for i in range(1000):
        print("Item:", i)
        page = try_request(dic['Title_URL'][i])
        soup = BeautifulSoup(page.content, 'html.parser')
        html_targets = {'num_reviews': soup.find('meta', itemprop = 'reviewCount'), 'num_pages': soup.find('span', itemprop = 'numberOfPages'), 'awards': soup.find('div', itemprop = 'awards'), 'genres': BeautifulSoup(str(soup.findAll('a', class_ = 'actionLinkLite bookPageGenreLink')[:3])), 'series': soup.find('h2', id = 'bookSeries'), 'year_published': soup.find('div', id = 'details'), 'places': soup.find('div', id = 'bookDataBox')}
        for column in list(dic.keys())[4:]:
            dic[column].append(check(html_targets[column]).get_text())
    pd.DataFrame(dic).to_csv('raw_scrap.csv')
    print("Time taken:", time.time() - t1, "seconds")

if __name__ == '__main__':
    scrap_goodreads_table('https://www.goodreads.com/list/show/5.Best_Books_of_the_Decade_2000s')    