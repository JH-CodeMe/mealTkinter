import tkinter as tk # tkinter 라이브러리를 추가하고 tk로 대체
import requests
from xml.etree import ElementTree as ET

API_KEY = "73977e5306894980844a1b64e662b879"

window = tk.Tk() # 창 생성
window.title("급식알리미") # 창의 이름을 급식알리미로 설정
window.geometry("640x400+100+100") # 창 크기 설정

entry = tk.Entry(window) # 텍스트 입력상자 생성
label = tk.Label(window, text="날짜를 8자리로 입력해주세요 ex)20210329")



def submit():
	ymd = tk.Entry.get(entry)
	if len(ymd) != 8:
		label.configure(text="날짜를 정확하게 입력해주세요")
	else:
		URL = "https://open.neis.go.kr/hub/mealServiceDietInfo?KEY="+API_KEY+"&Type=xml&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530525&MLSV_YMD="+ymd
		res = requests.get(URL)
		root = ET.ElementTree(ET.fromstring(res.text)).getroot()
		# 해당 날짜에 급식이 없을때 받는 응답:
		# <RESULT>
		# 	<CODE>INFO-200</CODE>
		# 	<MESSAGE>해당하는 데이터가 없습니다.</MESSAGE>
		# </RESULT> 
			
		if root.find("MESSAGE") != None:
			label.configure(text="해당 날짜에 데이터가 없습니다.")

		# 해당 날짜에 급식 있을때 받는 응답
		# <mealServiceDietInfo>
  		# 			<row>
  		#   			<DDISH_NM><![CDATA[j통새우튀김오므라이스1.2.5.6.9.10.12.13.15.16.<br/>j미소된장국5.6.8.9.13.<br/>j오이깍둑무침5.6.13.<br/>j파닭꼬치5.6.13.15.<br/>j깍두기9.13.<br/>j미니사과]]></DDISH_NM>
  		# 			</row>
		# </mealServiceDietInfo>

		else:
 			meallist = root.find("row").find("DDISH_NM").text.split("<br/>")
 			# <br/>를 기준으로 문자열을 나눠서 각각 급식을 리스트에 넣음
 			labeltext = ""
 			for i in meallist:
 				labeltext += i + "\n"
 			label.configure(text=labeltext)



button = tk.Button(window, text="제출", command=submit)

entry.pack() # 만든 Entry 배치
button.pack()
label.pack()

window.mainloop() # x 버튼 누를때까지 실행
