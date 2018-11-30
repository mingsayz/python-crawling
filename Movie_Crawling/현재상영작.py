import urllib.request
from datetime import datetime,date
import requests
import os
import sys
from bs4 import BeautifulSoup
import ast
from selenium import webdriver


# -*- coding: utf-8 -*-
a=0
client_id = "xu3aIzNFPuwE_QatTZdn"
client_secret = "lvGNtv3RtR"

def naver_parsing(string) :
	naver_html = naver_search_base + 'string'
	print(naver_html)
	naver_soup = BeautifulSoup(naver_html,"html.parser")
	return naver_soup


def change_xy(XY) :
	client_id = "ZBZRW93imkdPj8rZj96k"
	client_secret = "VH70zeukOD"
	encText = urllib.parse.quote(XY)
	url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
	# url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	response_body = response.read()
	soup_response = BeautifulSoup(response_body,'html.parser')
	source=str(soup_response)
	s_index=str(source).find('"x"')
	e_index=str(source).find('"y"')
	final_xy=str(source)[s_index : e_index+ 20].replace(" ","").replace('"','').replace("\n","")
	return final_xy

try :
	naver_search_base= "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
	url = "http://www.cgv.co.kr/movies/?ft=0"
	html = urllib.request.urlopen(url).read() #url 불러들여 html 변수에 저장
	soup = BeautifulSoup(html,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능
	li = soup.find_all("strong", {"class" : "title"})  # strong 에 class:title인 모든 태그를 긁어온다.
except :
	print("==============================================================\n")
	print("!!!!!!!!!!!!!!!!!!!네트워크 연결을 확인하세요!!!!!!!!!!!!!!!!\n ")
	print("==============================================================\n")
	exit()

count = 1

print("\n")

print("< 오늘은 몇일 ?! >" + " : " + str(datetime.date(datetime.now()))) #오늘 일자를 알려줌. 

print("\n")

print("----------현재상영작-------------\t")
print("\t\t\t\t |")
for name in li:
	print(str(count) + "위", name.get_text())
	print("\t\t\t\t |")
	count = count +1
print("---------------------------------\t") 

print("\n어떤 영화를 보고싶으세요 ?===> (그만두려면 '0'을 누르세요) ")
choice=input("\n숫자를 입력하세요 " + "("+"1~" + str((len(li)))+")"+ '중에 고르세요!======> ')
if choice == '0' :
	exit()


naver_link =naver_search_base + li[int(choice)-1].get_text()
input_choice=li[int(choice)-1].get_text()

#print(naver_link)
encText = urllib.parse.quote_plus(input_choice)
open_url = "https://openapi.naver.com/v1/search/movie?query=" + encText

request = urllib.request.Request(open_url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

#symbolslist = soup_response.find('table').tr.next_siblings
if(rescode==200):
	response_body=response.read()
	soup_response = BeautifulSoup(response_body,'html.parser')
	info = str(soup_response) #bs4 양식을 str 형태로 바꿔준다
	s_index = str(info).find('[') # items 는 []로 묶여있으므로 []의 좌표를 찾는다 
	e_index = str(info).find(']')
	movies = ast.literal_eval(info[s_index:e_index+1]) # 그부분을 리스트로 변환시켜준다.
	
	create_type = '<b>' + input_choice + '</b>'
	if create_type == movies[0]["title"]:
		print("\t이름: "+movies[0]["title"].replace('<b>','').replace('</b>',''))
		print("\t감독: "+movies[0]["director"].replace('|',''))
		print("\t개봉: "+movies[0]["pubDate"])
		print("\t평점: "+movies[0]["userRating"])
	else:
		print("!!!!!!!현재 개봉순위에서 사용자님께서 요청한 자료를 찾을수없습니다. 혹시 이중에 있습니까?!!!!!\n")
		print(info.replace('[','').replace('{','').replace('}','').replace(']','').replace('\n\n\n\n','\n'))
else :
    print("Error Code:" + rescode)


trailer_movie=input("\n예고편을 보시겠습니까? (y / n) ")

while (trailer_movie != 'n','N' ) :
	if trailer_movie == 'y' or trailer_movie == 'Y' :
		chrome_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'chromedriver')
		driver = webdriver.Chrome(chrome_path)	
		youtube_url= "https://www.youtube.com/results?search_query=" + input_choice + " 예고편"
		driver.set_page_load_timeout(30)
		driver.get(youtube_url)
		username = driver.find_element_by_css_selector('#thumbnail')
		username.click()
		break
	elif trailer_movie == 'n' or trailer_movie == 'N':
		print("\n그냥 계속 진행하겠습니다.")
		break
	else :
		print("잘못입력하셨습니다. 처음부터 다시 진행하세요.")
		trailer_movie=input("\n예고편을 보시겠습니까? (y / n) ")

searching_theater=input("\n주변의 영화관을 검색하시겠습니까? (y / n) ==>")
if searching_theater == 'y' or searching_theater == 'Y' :
	naver_maps= "http://map.naver.com/"
	chrome_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'chromedriver')
	driver = webdriver.Chrome(chrome_path)
	driver.implicitly_wait(3)
	driver.get(naver_maps)
	username=driver.find_element_by_css_selector("#search-input")
	username.send_keys("영화관")
	username=driver.find_element_by_css_selector("#header > div.sch > fieldset > button")
	username.click()

onetwo_choice=input("(1)여러 영화관 영화시간표 동시출력 (2) 하나의 영화관 출력")
# if onetwo_choice == '1' :

while True:

	print("=================================================================")
	theater=input("영화관을 선택하세요 (롯데시네마 ,cgv ,메가박스 중에 고르세요 !)	||=====>")
	print("=================================================================")
	enc_txt_theater = urllib.parse.quote_plus(theater) #urllib 라이브러리에 자동으로 utf-8 로 인코딩해주는 명령어 quote_plus를 써서 theater를 받는다.
	if (theater != '롯데시네마' and theater != 'cgv' and theater != '메가박스'):
		print("잘못된 영화관 이름입니다 !!!!")
	else : break

area_address=input("어느 "+ theater + "가 가고싶으신가요 ?"+" ex)동래, 수원 .. "+"=====>")
print("=================================================================\n")
enc_txt_area = urllib.parse.quote_plus(area_address)  #urllib 라이브러리에 자동으로 utf-8 로 인코딩해주는 명령어 quote_plus를 써서 지역를 받는다.

if theater == '롯데시네마' or theater == '메가박스' :
	count = 0;
	google_base ="https://www.google.com/search?ei=I8LrWqrgMsS3jwSv2pPwDQ&q="
	google_url=  google_base + enc_txt_theater + enc_txt_area 
	#print(google_url)
	headers = {'User-Agent' : 'test'}
	google_request = requests.get(google_url, headers=headers)
	google_soup= BeautifulSoup(google_request.text,'html.parser')
	#print(google_soup)
	google_li1 = google_soup.find_all("a",{"class":"fl X4s2nb"}) #영화 제목 리스트 생성
	google_li2 = google_soup.find_all("div",{"class":"e3wEkd"}) #영화 상영 시간표 리스트 생성
	for i in google_li1 :
		google_find = i.get_text().find(input_choice)
		if google_find == -1 :
			count = count + 1      #i 가 google_li1 리스트를 차례로 열면서 요청한 영화가 있는지 검색 없으면 count를 1 올린다.
		else : break
	if count == len(google_li1) :
		print(area_address +' '+ theater +"  에서는" + "요청하신 " + input_choice +"을(를) 상영하지 않습니다 ㅠㅠ") #카운트로 있는지 없는지 체크할수있다.
		sys.exit()
	else :
		print(area_address+ ' '+ theater +'에서의'+' '+input_choice+' 상영예정시간은 다음과 같습니다.\n\n'+google_li2[count].get_text().replace('am','am\t').replace('pm','pm\t'))
elif theater == 'cgv' :
	date= datetime.date(datetime.now())
	cgv_date=str(date).replace("-","")
	naver_cgv = naver_search_base + enc_txt_theater + enc_txt_area
	print(naver_cgv)
	search_cgv = urllib.request.urlopen(naver_cgv).read() #url 불러들여 html 변수에 저장
	parser_cgv = BeautifulSoup(search_cgv,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능
	li_cgv0=parser_cgv.find("div",class_="sp_website section")
	li_cgv1=li_cgv0.get_text()
	li_cgv2=li_cgv1.find("theaterCode=")
	cgv_theaternum=li_cgv1[li_cgv2+12:li_cgv2+16]
	cgv_base ="http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?&theatercode="
	cgv_url = cgv_base+str(cgv_theaternum)+"&date="+str(cgv_date)+"&screencodes=&screenratingcode=&regioncode="
	#print(cgv_url)
	cgv_html = urllib.request.urlopen(cgv_url).read() #url 불러들여 html 변수에 저장
	cgv_soup = BeautifulSoup(cgv_html,"html.parser")
	cgv_li=cgv_soup.find_all("div",{"class":"col-times"})
	for i in cgv_li :
		time_table = i.get_text()
		if time_table.find(input_choice) != -1 : 
			print(time_table.replace(" ","").replace("\n\n\n\n","").replace("\n\n\n","\n--------------").replace("\n\n","\n----------------"))
			a=a+1
	if len(cgv_li)-a == len(cgv_li):
		print("=================================================================")
		print(area_address + theater + "에는 요청하신 영화를 상영하지 않습니다 ㅠㅠ")
		print("=================================================================\n")

		sys.exit()

else : 
	print("잘못 입력하셨습니다! 다시 시도해주세요 ㅎ_ㅎ")
	exit()

mapping_choice=input("\ngoogle map에서 거리를 검색하시겠습니까? (y / n) ==>")
if mapping_choice == 'y' or mapping_choice == 'Y' :
	where_are_u = input("\n지금 어디에 계십니까? ==>")
	url_maps= "https://www.google.com/maps/dir///@37.5575956,-122.289169,15z"
	chrome_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'chromedriver')
	driver = webdriver.Chrome(chrome_path)
	driver.implicitly_wait(3)
	driver.get(url_maps)
	username=driver.find_element_by_css_selector("#sb_ifc50 > input")
	username.send_keys(where_are_u)
	username=driver.find_element_by_css_selector("#sb_ifc51 > input")
	username.send_keys(area_address+theater)
	username=driver.find_element_by_css_selector("#directions-searchbox-1 > button.searchbox-searchbutton")
	username.click()

#http://www.lottecinema.co.kr/LCHS/Contents/ticketing/ticketing.aspx 롯데시네마
#http://www.cgv.co.kr/ticket/
#http://www.megabox.co.kr/?show=booking&p=step1

ticketing = input("\n예매 하시겠습니까? ( y / n )")

while (ticketing != 'n','N' ) :
	if ticketing == 'y' or ticketing == 'Y' :
		chrome_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'chromedriver')
		driver = webdriver.Chrome(chrome_path)	
		if theater == '롯데시네마' :	
			ticketing_url= "http://www.lottecinema.co.kr/LCHS/Contents/ticketing/ticketing.aspx"
			driver.set_page_load_timeout(30)
			driver.get(ticketing_url)
			break
		elif theater == 'cgv' :
			ticketing_url= "http://www.cgv.co.kr/ticket/"
			driver.set_page_load_timeout(30)
			driver.get(ticketing_url)
			break
		else :
			ticketing_url= "http://www.megabox.co.kr/?show=booking&p=step1"
			driver.set_page_load_timeout(30)
			driver.get(ticketing_url)
			break

	elif ticketing == 'n' or ticketing == 'N':
		print("즐거운 관람 되십시오!")
		break
	else :
		print("잘못입력하셨습니다. 처음부터 다시 진행하세요.")
		ticketing = input("\n예매 하시겠습니까? ( y / n )")




# else : print("프로그램을 종료합니다 !") 


#  ===============================googld maps 가져오기 x,y 좌표 필요없음 ===================================================
# add_XY = input("어디에 계신가요 ?")
# Now_XY =change_xy(add_XY)

# add1_XY = input("어디로 가시나요?")
# Des_XY = change_xy(add1_XY)

# print(Now_XY,Des_XY)

# ---------------------------google maps 가져오기 -------------------
# gps 
# address=input("영화관을 선택하세요! :")
# enc_txt_gps = urllib.parse.quote_plus(address) # encoding 하여 enc_txt 라는 변수에 넣어둔다.
# gps_address = naver_search_base + enc_txt # 미리 정해둔 naver_search_base 에 encoding된 chg_txt를 더한다
# gps_html = urllib.request.urlopen(gps_address).read().decode('utf8') #
# gps_soup = BeautifulSoup(gps_html,"html.parser") # html 형식으로 파싱
# gps_if = gps_soup.find("div",class_="dti_box") # div 태그 안에 class 가 dti_box 인 것을 끌어온다.
# gps_if1 = gps_if.find("dd") # 그안에서 필요한것은 주소뿐이므로 dd 태그를 끌어온다.
# gpsFinal=gps_if1.get_text() # 태그를 빼고 안에 contents 만 출력한다.

# print("\n")

# date= datetime.date(datetime.now())
# cgv_date=str(date).replace("-","")


# ----------------------naver open api ---------------------
# naver open api gps ID,PASSWD
# api_ID="ZBZRW93imkdPj8rZj96k"
# api_Passwd="VH70zeukOD"
# gps_encText = urllib.parse.quote_plus(address)
# gps_url = "https://openapi.naver.com/v1/map/geocode?query=" + gps_encText # json 결과
# # url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
# gps_request = urllib.request.Request(gps_url)
# gps_request.add_header("X-Naver-Client-Id",api_ID)
# gps_request.add_header("X-Naver-Client-Secret",api_Passwd)
# gps_response = urllib.request.urlopen(gps_request)
# gps_rescode = gps_response.getcode()
# if(gps_rescode==200):
#     gps_response_body = gps_response.read()
#     print(gps_response_body.decode('utf-8'))
# else:
#     print("Error Code:" + gps_rescode)



