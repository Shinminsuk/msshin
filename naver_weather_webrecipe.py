# 파이썬 레시피 - 웹 활용 입문편
# https://wikidocs.net/book/2965

from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests

html = requests.get('https://search.naver.com/search.naver?query=날씨')
# pprint(html.text)

soup = bs(html.text,'html.parser')

data1 = soup.find('div',class_='detail_box')
data2 = soup.find_all('dd', class_='lv1')

pprint(data1.text)
pprint(len(data2))
pprint(data2[0].text)

#a = ""
#for i in data2 :
#    a += i.text
#print(a)

