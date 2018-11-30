import urllib.request
from datetime import datetime,date
import requests
import os
import sys
from bs4 import BeautifulSoup
import ast

url = "https://map.naver.com/"
html = urllib.request.urlopen(url).read() #url 불러들여 html 변수에 저장
soup = BeautifulSoup(html,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능
print(soup)