# 멀티캠퍼스 파이썬 웹크롤링 강의
# 18차시 : 구글 이미지 크롤러


#Step 1. 필요한 모듈과 라이브러리를 로딩합니다.

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import urllib
import sys
import re
import math
import time
import os
import random
from selenium.webdriver.common.keys import Keys
import dload  # 3.6버전 이상부터 (스파르타에서 이미지 다운로드시 사용)

#import urllib.request
#import urllib

#Step 2. 필요한 정보를 입력 받습니다.
print("=" *80)
print("구글 사이트에서 이미지를 검색하여 수집하는 크롤러 입니다 ")
print("=" *80)

# query_txt = input('1.크롤링할 이미지의 키워드는 무엇입니까?: ')
# cnt = int(input('2.크롤링 할 건수는 몇건입니까?: '))
# f_dir=input('3.파일이 저장될 경로만 쓰세요(예: c:\\doit\\data\\ ) : ')

query_txt = '캘리그라피' #input('1.크롤링할 이미지의 키워드는 무엇입니까?: ')
cnt = 51
f_dir=''
if f_dir =='' :
    f_dir = "c:\\doit\\data\\"
    print(f_dir, '에 저장됩니다. ')

print("\n")
print("요청하신 데이터를 수집 중이오니 잠시만 기다려 주세요~~^^")

real_cnt = math.ceil(cnt / 50) # 실제 크롤링 할 페이지 수

#Step 3. 파일을 저장할 폴더를 생성합니다
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min) #now.tm_sec

os.chdir(f_dir)
os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)
f_result_dir = f_dir+s+'-'+query_txt
f_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'

#Step 4. 크롬 드라이버를 사용해서 웹 브라우저를 실행한 후 검색합니다

s_time = time.time( )

path = "c:/doit/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get('https://www.google.com')
time.sleep(random.randrange(2, 5))

element = driver.find_element_by_name("q")

element.send_keys(query_txt)
#element.submit()
element.send_keys('\n')

# 소주제 1: 자동 스크롤 다운 기능을 구현하여 화면을 자동으로 스크롤링하기

# Step 5. 아래의 이미지 링크를 선택합니다

driver.find_element_by_link_text("이미지").click()

time.sleep(random.randrange(2, 5))


# 스크롤 다운 함수 만들기

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(3)


i = 1
while (i <= real_cnt):
    scroll_down(driver)
    i += 1

    if i == 6:
        driver.find_element_by_xpath("""//*[@id="_sau_imageTab"]/div[2]/div[8]/a""").click()

# 소주제 2: 이미지 URL 을 참고하여 그림을 추출한 후 저장하기

# Step 6. 이미지 추출하여 저장하기

#file_no = 0
file_no = 1
count = 1
img_src2 = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# 원코드
imgs = driver.find_elements_by_tag_name('img')

for img in imgs:
    img_src1 = img.get_attribute('src')
    img_src2.append(img_src1)
    count += 1

print(len(img_src2))

#driver.back( )

for i in range(2, len(img_src2) + 1):

    try:
        urllib.request.urlretrieve(img_src2[i], str(file_no) + '.jpg')
#        dload.save(img_src2[i], str(file_no) + '.jpg')
    except TypeError:
        continue

    file_no += 1

    time.sleep(1)
    print("\n")
    print("%s 번째 이미지 저장중입니다=======" % file_no)
    print("\n")

    if file_no == cnt:
        break
# 여기 까지 원코드

# 스파르타 소스시작  # 에러가 나는데 주소가 잘못됐나? 'img'

# imgs = soup.select('#islrg > div.islrc > img')
#
# for img in imgs:
#     src = img['src']
#     dload.save(src, f'imgs/{file_no}.jpg')
#     file_no += 1
# 스파르타 소스끝

#링크리스트를 txt 파일로
f = open(f_name, 'a',encoding='UTF-8')
f.write(str(img_src2))
f.close( )

# Step 7. 요약 정보를 출력합니다
e_time = time.time( )
t_time = e_time - s_time

store_cnt = file_no -1

print("=" *70)
print("총 소요시간은 %s 초 입니다 " %round(t_time,1))
print("총 저장 건수는 %s 건 입니다 " %file_no)
print("파일 저장 경로: %s 입니다" %f_result_dir)
print(" txt 파일 저장 경로: %s" %f_name)
print("=" *70)

driver.close( )
