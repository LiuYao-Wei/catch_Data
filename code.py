import requests
import json
#--------------Air quality-----------------
def dataOfAir():
  url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
  response = requests.get(url)
  data = response.json()
  while True:
    county_set = set()
    #sitename_set = set()
    #--------------以下為印出總區域-----------------------
    for i in data['records']:
      county_set.add(i['county'])
    county_list = list(county_set)
    for i in range(len(county_list)):
      print(i+1,county_list[i])
    implementEvent = int(input('請輸入需要查詢的縣市代號:'))
    #---------------------以上----------------------------
    sitename_list = [i['sitename'] for i in data['records'] if i['county'] == county_list[implementEvent-1]]
    #----------如果該地區只有一個測站直接印出-------------
    if len(sitename_list) == 1:
      for i in data['records']:
        if i['sitename'] == sitename_list[0]:
          print(i['county'] + ' ' + i['sitename'])
          print('AQI:' + i['aqi'] + ' ' + '空氣品質' + i['status'])
          print('細懸浮微粒PM2.5:' + i['pm2.5'] + '(μg/m3)' + '  ' + '懸浮微粒PM10:' + i['pm10'] + '(μg/m3)')
          print('二氧化硫SO2:' + i['so2'] + '(ppb)' + '       ' + '氮氧化物NOx:' + i['nox'] + '(ppb)')
          print('臭氧O3:' + i['o3'] + '(ppb)' + '           ' + '一氧化碳CO:' + i['co'] + '(ppm)')
    #---------------------以上----------------------------
    else:
    #-----------以下為找出該縣市的所有測站----------------
      #chToDo為是否要找全部測站的代號
      chToDo = int(input('如果要找該縣市所有測站請按0；要找特定測站請按1:'))
      if chToDo == 0:
        print(county_list[implementEvent-1])
        for i in data['records']:
          if i['county'] == county_list[implementEvent-1]:
            print("測站名稱:" + i['sitename'] + " " + "AQI:" + i['aqi'] + " " + "空氣品質:" + i['status'])
    #---------------------以上----------------------------
    #--------------找出此縣市內的所有測站-----------------
      elif chToDo == 1:
        #sitename_list = [i['sitename'] for i in data['records'] if i['county'] == county_list[implementEvent-1]]
        for i in range(len(sitename_list)):
          print(i+1,sitename_list[i])
    #---------------------以上----------------------------
        sitename_num = int(input('請輸入需要查詢的測站代號:'))
    #-----------------印出該站的資料----------------------
        for i in data['records']:
          if i['sitename'] == sitename_list[sitename_num-1]:
            print(i['county'] + ' ' + i['sitename'])
            print('AQI:' + i['aqi'] + ' ' + '空氣品質' + i['status'])
            print('細懸浮微粒PM2.5:' + i['pm2.5'] + '(μg/m3)' + '  ' + '懸浮微粒PM10:' + i['pm10'] + '(μg/m3)')
            print('二氧化硫SO2:' + i['so2'] + '(ppb)' + '       ' + '氮氧化物NOx:' + i['nox'] + '(ppb)')
            print('臭氧O3:' + i['o3'] + '(ppb)' + '           ' + '一氧化碳CO:' + i['co'] + '(ppm)')
    #---------------------以上----------------------------
    repeat = int(input('要重新查詢請按0，要結束查詢請按1:'))
    if repeat == 0:
      continue
    elif repeat == 1:
      break
#--------Air quality finish here-----------

#---------------YouBike Data--------------- 
def dataOfBike():
  url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
  response = requests.get(url)
  data = response.json()
  #-----------以下為查詢總區域並印出--------------------
  sarea_data = [station['sarea'] for station in data]
  sareaData = set()
  for sarea in sarea_data:
    sareaData.add(sarea)
  sarea_list = list(sareaData)
  while True:
    #print("請輸入需要查詢的地區代號或使用路名查詢:")
    for i in range(len(sarea_list)):
      print(i+1,sarea_list[i])
    print(len(sarea_list)+1,"使用路名查詢")
    print(len(sarea_list)+2,"使用站名查詢")
  #---------------------以上----------------------------
    #implementEvent為處理的事件代號
    implementEvent = int(input("請輸入需要查詢的地區代號或使用路名查詢:"))
  #------------------使用區域查詢-----------------------
    if implementEvent != len(sarea_list)+1 and implementEvent != len(sarea_list)+2:
      #sna:站點名稱, sbi:目前可借數量, bemp:空位數量, ar:站點地址
      main_data = [(station['sna'], station['sbi'], station['bemp'], station['ar']) for station in data if station.get('sarea') == sarea_list[implementEvent-1]]
      for sna, sbi, bemp, ar in main_data:
        print("站點名稱: ",sna,"\n目前可借數量: ",sbi,"\n可停空位數量: ",bemp,"\n站點地址: ",ar,"\n")
      n = int(input("重新輸入請按1，不要請按0:"))
      if n == 1:
        continue
      else:
        break
  #---------------------以上---------------------------
  #-----------------使用路名查詢-----------------------
    elif implementEvent == len(sarea_list)+1:
      print("如果在trinket上執行中文會有空格問題，請於其它地方複製路名再到此處貼上")
      rdName = input("輸入路名:")
      main_data = [(station['sna'], station['sbi'], station['bemp'], station['ar']) for station in data if rdName in station.get('ar')]
      if not main_data:
        print("此路段無YouBike站點")
      else:
        for sna, sbi, bemp, ar in main_data:
          print("站點名稱: ",sna,"\n目前可借數量: ",sbi,"\n可停空位數量: ",bemp,"\n站點地址: ",ar,"\n")
      n = int(input("重新輸入請按1，不要請按0:"))
      if n == 1:
        continue
      else:
        break
  #---------------------以上---------------------------
  #-----------------使用站名查詢-----------------------
    elif implementEvent == len(sarea_list)+2:
      print("如果在trinket上執行中文會有空格問題，請於其它地方複製路名再到此處貼上")
      siteName = input("輸入站名:")
      main_data = [(station['sna'], station['sbi'], station['bemp'], station['ar']) for station in data if siteName in station.get('sna')]
      if not main_data:
        print("查無此YouBike站點")
      else:
        for sna, sbi, bemp, ar in main_data:
          print("站點名稱: ",sna,"\n目前可借數量: ",sbi,"\n可停空位數量: ",bemp,"\n站點地址: ",ar,"\n")
      n = int(input("重新輸入請按1，不要請按0:"))
      if n == 1:
        continue
      else:
        break
  #---------------------以上---------------------------
#--------YouBike Data finish here----------

#-------------exchange rate---------------- 
def exchangeRate():
  url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
  rate = requests.get(url)
  rate.encoding = 'utf-8'
  rt = rate.text
  rts = rt.split('\n')
  for i in rts:              # 讀取串列的每個項目
    try:                             # 使用 try 避開最後一行的空白行
        a = i.split(',')             # 每個項目用逗號拆分成子串列
        if a[12] == '現金':
          print(a[0] + ': ' + '買入金額' + '\t' + '賣出金額')
        else:
          print(a[0] + ': ' + a[2] + '\t',end='')   # 取出第一個 ( 0 ) 和第十三個項目 ( 12 )
          print(a[12])
    except:
      break
#--------exchange rate finish here---------

while True:
  print("1: Youbike即時資訊系統\n2: 空氣品質\n3: 台灣銀行匯率")
  need_do = int(input("請輸入需要查詢的代號:"))
  
  if need_do == 1:
    dataOfBike()
    finil_do = int(input("回首頁請按1，要結束請按0:"))
    if finil_do == 0:
      break
    elif finil_do == 1:
      continue
  # --------以下需要修改--------
  if need_do == 2:
    dataOfAir()
    finil_do = int(input("回首頁請按1，要結束請按0:"))
    if finil_do == 0:
      break
    elif finil_do == 1:
      continue
  if need_do == 3:
    exchangeRate()
    finil_do = int(input("回首頁請按1，要結束請按0:"))
    if finil_do == 0:
      break
    elif finil_do == 1:
      continue




