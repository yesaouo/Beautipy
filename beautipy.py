import json, requests
from bs4 import BeautifulSoup

def checkJSONFile(fileName):
  try:
    with open(fileName,'r',encoding='utf-8') as f:
      return json.load(f)
  except FileNotFoundError:
    with open(fileName,'w',encoding='utf-8') as f:
      json.dump({},f)
    return {}

def getPage():
  web = requests.get('https://www.ptt.cc/bbs/Beauty/index.html', cookies={'over18':'1'})
  soup = BeautifulSoup(web.text, "html.parser")
  btn_wide = soup.find_all('a', class_='btn wide')
  for i in btn_wide:
    if i.get_text() == '‹ 上頁':
      newPage = int(i['href'].replace('/bbs/Beauty/index','').replace('.html','')) + 1
      return newPage
  return 1

def crawlPTT(page,newPage):
  ban = ['[公告]','[帥哥]','大尺碼']
  img_url = checkJSONFile('image.json')
  new_img = {}
  newImg = []

  for i in range(newPage,newPage-page,-1):
    web = requests.get(f'https://www.ptt.cc/bbs/Beauty/index{i}.html', cookies={'over18':'1'})
    soup = BeautifulSoup(web.text, "html.parser")
    titles = soup.find_all('div', class_='title')
    for i in titles:
      find_a = i.find('a')
      if find_a:
        text_a = find_a.get_text()
        if find_a != None and not any([e in text_a for e in ban]) and not img_url.get(text_a):
          new_img[text_a]=['https://www.ptt.cc/' + find_a['href']]

  if new_img:
    print("新增的:")
    for title in new_img:
      print(title)
      web = requests.get(new_img[title][0], cookies={'over18':'1'})
      soup = BeautifulSoup(web.text, "html.parser")
      imgs = soup.find_all('img')
      imgList = []
      for i in imgs:
        newImg.append(i['src'])
        imgList.append(i['src'])
      new_img[title].append(imgList)

  if img_url:
    print("已上傳的:")
    for title in img_url:
      print(title)
  img_url.update(new_img)
  with open('image.json','w',encoding='utf-8') as f:
    json.dump(img_url,f,indent=1,ensure_ascii=False)
  
  print(f'爬取完成，新增了 {len(newImg)} 張圖片')

crawlPTT(int(input('爬取頁數(圖多注意): ')),getPage())