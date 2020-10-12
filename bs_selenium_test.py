## 한국 관광공사 웹크롤링
# c:\doit\ 폴더가 작업 폴더, c:\doit\data\ 폴더가 데이터 저장 폴더

## Step 0. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다

from bs4 import BeautifulSoup     
from selenium import webdriver
import time
import sys
import os
import re
import math
import numpy
import pandas as pd
import xlwt

##Step 2. 사용자에게 검색어 키워드를 입력 받습니다.
print("=" *80)
print("대한민국 구석구석 사이트의 모든 여행지 정보 수집하기")
print("=" *80)

query_txt = input('크롤링할 키워드는 무엇입니까?: ')
#query_txt = '가을 여행'

f_dir = input("결과 파일을 저장할 폴더명만 쓰세요(없으면 :c:\\doit\\data\\):")

if f_dir == '':
    f_dir = "C:\\doit\\data\\"

# 저장될 파일위치와 이름을 자동 지정합니다
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)

ff_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'
fx_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'
fc_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'

#ff_name = input('검색 결과를 저장할 txt 파일경로와 이름을 지정하세요(예:c:\\temp\\test.txt): ') # txt 파일 이름
#fc_name = input('검색 결과를 저장할 csv 파일경로와 이름을 지정하세요(예:c:\\temp\\test.csv): ') # csv 파일 이름
#fx_name = input('검색 결과를 저장할 xls 파일경로와 이름을 지정하세요(예:c:\\temp\\test.xls): ') # xls 파일 이름

##Step 3. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
path = "c:/doit/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://korean.visitkorea.or.kr/main/main.html")
time.sleep(2)  # 창이 모두 열릴 때 까지 2초 기다립니다.

#코로나 안내 팝업창 있을 경우 닫기 클릭하기 
try :
    driver.find_element_by_xpath('//*[@id="safetyStay1"]/div/div/div/button').click()
except :
    print("안내 팝업창이 없습니다")
    
##Step 4. 검색창의 이름을 찾아서 검색어를 입력합니다

#driver.find_element_by_id("btnSearch").click()  ## 검색 디폴트값에 따라 움직이는데 예외처리 방법으로 해결?

driver.find_element_by_id("btnSearch").click()
element = driver.find_element_by_id("inp_search")

try :
    element.send_keys(query_txt)  # 검색 단추가 없어서 에러나면 다시 한번 눌러서 검색창을 띠움
except:
    driver.find_element_by_id("btnSearch").click()
    element = driver.find_element_by_id("inp_search")
    element.send_keys(query_txt)

#Step 3. 검색 버튼을 눌러 실행합니다
driver.find_element_by_link_text("검색").click()

# Step 4. 현재 페이지에 있는 내용을 화면에 출력하기

time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find('ul',class_='list_thumType flnon')

# print(content_list)

# 소주제 1: 특정 항목들을 분리해서 추출하기
no = 1
no2 =[ ]
contents2=[ ]
tags2=[ ]

for i in content_list:
    no2.append(no)
    print('번호:',no)
    
    contents = i.find('div','tit').get_text( )
    contents2.append(contents)
    print('내용:',contents.strip())
    
    tag = i.find('p','tag').get_text()
    tags2.append(tag)
    print('태그:',tag.strip())
    print("\n")
    
    no += 1
    
# 소주제 2: 분리 수집된 데이터를 데이터 프레임으로 만들어서 csv , xls 형식으로 저장하기
# 출력 결과를 txt 파일로 저장하기
f = open(ff_name, 'a',encoding='UTF-8')
f.write(str(contents2))
f.write(str(tags2))
f.close( )
print(" txt 파일 저장 경로: %s" %ff_name)    
    
# 출력 결과를 표(데이터 프레임) 형태로 만들기
import pandas as pd

korea_trip = pd.DataFrame()
korea_trip['번호']=no2
korea_trip['내용']=contents2
korea_trip['태그']=tags2

# csv 형태로 저장하기
korea_trip.to_csv(fc_name,encoding="utf-8-sig")
print(" csv 파일 저장 경로: %s" %fc_name)

# 엑셀 형태로 저장하기
import xlwt   # pip install xlwt 실행 후 수행
korea_trip.to_excel(fx_name)
print(" xls 파일 저장 경로: %s" %fx_name)

