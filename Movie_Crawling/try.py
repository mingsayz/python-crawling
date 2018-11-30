import urllib.request
from datetime import datetime,date
import requests
from bs4 import BeautifulSoup
import osㅠㅎ
import sys

client_id = "xu3aIzNFPuwE_QatTZdn"
client_secret = "lvGNtv3RtR"

def naver_parsing(naver_link) :
	naver_html = requests.get(naver_link).content
	naver_soup = BeautifulSoup(naver_html,"html.parser")
	return naver_soup


naver_search_base = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
url = "http://www.cgv.co.kr/movies/?ft=0"
html = urllib.request.urlopen(url).read() #url 불러들여 html 변수에 저장
soup = BeautifulSoup(html,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능

 
li = soup.find_all("strong", {"class" : "title"})  # strong 에 class:title인 모든 태그를 긁어온다.
count = 1

print("< 오늘은 몇일 ?! >" + " : " + str(datetime.date(datetime.now()))) #오늘 일자를 알려줌. 


print("\t----현재상영작----\t")

for name in li:
   print(str(count) + "위", name.get_text())
   count = count +1
 

print("\n어떤 영화를 보고싶으세요 ?===> (그만두려면 '0'을 누르세요) " + "1~" + str((len(li))) )
choice=input("\n숫자를 입력하세요 : ")


naver_link =naver_search_base + li[int(choice)-1].get_text()
print(naver_link)
#main_pack > div.movie_info.section > div.info_main > dl.r_grade
#naver_rating=naver_parsing(naver_link).find_all	("div",{"class":"movi_info section"})
#new_rating=BeautifulSoup(str(naver_rating),'html.parser')
#rating = new_rating.find_all('em')
#print(naver_rating)

# file = open("C:/Users/kaosa/OneDrive/Desktop/공부자료/movie.txt", "w", encoding='utf-8')
# headers = {
#     'Host' : 'openapi.naver.com',
#     'User-Agent' : 'curl/7.43.0',
#     'Accept' : '*/*',
#     'Content-Type' : 'application/xml',
#     'X-Naver-Client-Id' : 'xu3aIzNFPuwE_QatTZdn',
#     'X-Naver-Client-Secret' : 'lvGNtv3RtR'
#  }



print(naver_rating)
    for i in naver_rating :
    	search_em = i.get_text()
    	print(search_em)



import json

mytext = '{"title":"hwi","link":"http://hwi.com"}'
obj = json.loads(mytext)
print(obj["title"])




for movie in soup_response.find_all("items"):
		print(movie)
		for tag in movie.contents:
			if isinstance(tag, NavigableString):
				index = str(tag).find("userRating")
				print(index)
				if index != -1:
					m_index = index+len("userRating")+4
					print(str(tag)[m_index:m_index+4])




response_body = response.read()
   soup_response = BeautifulSoup(response_body,'lxml')
   info = str(soup_response)
   s_index = str(info).find('[')
   e_index = str(info).find(']')
   movies = ast.literal_eval(info[s_index:e_index+1])
   print("감독: "+movies[0]["director"])
   print("평점: "+movies[0]["userRating"])