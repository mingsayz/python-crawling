import urllib.request
from datetime import datetime,date
import requests
import os
import sys
from bs4 import BeautifulSoup
import ast
from selenium import webdriver

a=0
client_id = "xu3aIzNFPuwE_QatTZdn"
client_secret = "lvGNtv3RtR"

def naver_parsing(string) :
	naver_html = naver_search_base + 'string'
	print(naver_html)
	naver_soup = BeautifulSoup(naver_html,"html.parser")
	return naver_soup


naver_search_base= "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="
url = "http://www.cgv.co.kr/movies/?ft=0"
html = urllib.request.urlopen(url).read() #url 불러들여 html 변수에 저장
soup = BeautifulSoup(html,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능

 
li = soup.find_all("strong", {"class" : "title"})  # strong 에 class:title인 모든 태그를 긁어온다.
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
choice=input("\n숫자를 입력하세요 :" + "("+ "1~" + str((len(li)))+ '중에 고르세요!'+")")
if choice == '0' :
	exit()


naver_link =naver_search_base + li[int(choice)-1].get_text()
input_choice=li[int(choice)-1].get_text()

print(naver_link)

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
		print("\t감독: "+movies[0]["director"])
		print("\t개봉: "+movies[0]["pubDate"])
		print("\t평점: "+movies[0]["userRating"])
	else:
		print("\n\n")
		print("!!!!!!!현재 개봉순위에서 사용자님께서 요청한 자료를 찾을수없습니다. 혹시 이중에 있습니까?!!!!!\n")
		print(info)		
else :
    print("Error Code:" + rescode)


# gps 
address=input("영화관을 선택하세요! :")
enc_txt = urllib.parse.quote_plus(address) # encoding 하여 enc_txt 라는 변수에 넣어둔다.
# gps_address = naver_search_base + enc_txt # 미리 정해둔 naver_search_base 에 encoding된 chg_txt를 더한다
# gps_html = urllib.request.urlopen(gps_address).read().decode('utf8') #
# gps_soup = BeautifulSoup(gps_html,"html.parser") # html 형식으로 파싱
# gps_if = gps_soup.find("div",class_="dti_box") # div 태그 안에 class 가 dti_box 인 것을 끌어온다.
# gps_if1 = gps_if.find("dd") # 그안에서 필요한것은 주소뿐이므로 dd 태그를 끌어온다.
# gpsFinal=gps_if1.get_text() # 태그를 빼고 안에 contents 만 출력한다.

print("\n")

date= datetime.date(datetime.now())
cgv_date=str(date).replace("-","")


naver_cgv = naver_search_base + enc_txt
print(naver_cgv)
search_cgv = urllib.request.urlopen(naver_cgv).read() #url 불러들여 html 변수에 저장
parser_cgv = BeautifulSoup(search_cgv,"html.parser") # html.parser 로 파싱 , xml 형식으로도 가능
#print(soup_cgv)
li_cgv0=parser_cgv.find("div",class_="sp_website section")
li_cgv=li_cgv0.get_text()
li_cgv1=li_cgv.find("theaterCode=")
print(li_cgv[li_cgv1+12:li_cgv1+16])


print(li_cgv)

index1 = li_cgv.find("=")
number_cgv = li_cgv[index1+1:index1+5]

cgv_base ="http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?&theatercode="
cgv_url = cgv_base+str(number_cgv)+"&date="+str(cgv_date)+"&screencodes=&screenratingcode=&regioncode="
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
	print(address + "에는 요청하신 영화를 상영하지 않습니다 ㅠㅠ")

# if fail_find == -1 :
# 	print(address + "에는 요청하신 영화를 상영하지 않습니다 ㅠㅠ")
		
	# 	continue
	# if find_choice == -1 :
	# 	print(address + "에는 요청하신 영화를 상영하지 않습니다.")
	# else :
	# 	print("성공")

	#print(time_table.replace(" ",''))
# for div in cgv_soup.find_all("div",{"class":"col-times"}):
# 	print(div.get_text()
	# li = div.find_all('em')
	# li2 = BeautifulSoup(str(li),'html.parser')
	# print(li2.get_text())


# choice_add=input("당신은 어디에 계신가요? :")

# print("\n")

# url= "https://map.naver.com/"
# driver = webdriver.Chrome("C:\\Users\\kaosa\\OneDrive\\Desktop\\Movie_Crawling\\chromedriver_win32\\chromedriver.exe")
# driver.implicitly_wait(3)
# driver.get(url)
# username=driver.find_element_by_css_selector("#nav > ul > li:nth-child(2)")
# username.click()
# username=driver.find_element_by_css_selector("#panel > div.panel_content.nano.has-scrollbar > div.scroll_pane.content > div.panel_content_fixed > div.panel_findway_top > div.pf_enter > div:nth-child(1) > span > input")
# username.send_keys(choice_add)
# username=driver.find_element_by_css_selector("#panel > div.panel_content.nano.has-scrollbar > div.scroll_pane.content > div.panel_content_fixed > div.panel_findway_top > div.pf_enter > div:nth-child(2) > span > input")
# username.send_keys(gpsFinal)
# username=driver.find_element_by_css_selector("#panel > div.panel_content.nano.has-scrollbar > div.scroll_pane.content > div.panel_content_fixed > div.panel_findway_top > div.pf_act > a.spm.spm_pfa_startfind.spm_pfa_startfind_dimmed.nclicks\28 sfd\2e goroute\29")
# username.click()	


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


