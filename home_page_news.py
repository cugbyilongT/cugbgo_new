import os
import bs4
import requests
from bs4 import BeautifulSoup
def get_news_page(url):
      try:
            kv = {'User-agent':'Chrome/10'}
            res = requests.get(url,headers=kv)
            res.raise_for_status
            res.encoding=res.apparent_encoding 
            return res 
      except:
            return ''
      return ''
def get_news(url,title,path):
      new_path =path + title+'.txt'
      if os.path.exists(new_path):
            print(title+'  新闻已存在')
            return ;
      try:
            kv = {'User-agent':'Chrome/10'}
            res = requests.get(url,headers=kv)
            res.raise_for_status
            #print(res.raise_for_status)
            res.encoding=res.apparent_encoding
      except:
            return ''
      html = BeautifulSoup(res.text,'html.parser')
      
      time = html.find(attrs={'class':'date'})
      sourse = html.find(attrs = {'class':'text_gray'})
      time='发布时间:'+time.text
      sourse = sourse.text
      #print(sourse)
      try:
            f = open(new_path,'w',encoding='utf-8')
            f.write(time+'\n')
            f.write(sourse+'\n')
            news = html.find(attrs={'class':'content'})
            #for pic in news.findAll('img'):
            #      f.write(pic['src']+'\n')
            for p in news.children:
                  if type(p)==bs4.element.Tag:
                        if not p.find('img')==None:
                              pic = p.find('img')
                              f.write('图片:'+pic['src']+'\n')
                        else:
                              f.write('\n'+'  '+p.text+'\n')
            f.close()
      except:
            print(title+'  新闻写入失败')
      return ''
def handle_news_2(html,news_type):
      path = 'D://123/'+news_type+'/'
      #print(path)
      try:
            if not os.path.exists (path):
                  os.mkdir(path)
      except:
            print('文件创建失败')
      for a in html.findAll('a'):
            news_url=a["href"]
            news_title=a["title"]
            #print(news_url)
            get_news(news_url,news_title,path)
                        
            
                        
      
      return ''
def handle_news_1(html,news_type):
      path = 'D://123/'+news_type+'/'
      #print(path)
      try:
            if not os.path.exists (path):
                  os.mkdir(path)
      except:
            print('文件创建失败')
      html = html.find(attrs ={'class':'thumb'})
      for a in html.findAll('a'):
            news_url = a['href']
            news_title=a.find('img')['alt']
            get_news(news_url,news_title,path)
            
      return ''
def get_news_url(html):
      soup = BeautifulSoup(html.text,'html.parser')
      classname = ['deptinfo','collegeinfo','school','media','cugbpic','corner']
      for news_type in classname:
            news = soup.find(attrs={'class':news_type})
            #print(type(news))
            if news_type=='cugbpic':
                  handle_news_1(news,news_type)
            else:
                  handle_news_2(news,news_type)
            
            
      return ''
      
def get_news_list(url):
      html = get_news_page(url)
      get_news_url(html)
      return''
      
def main():
      url = 'http://www.cugb.edu.cn/news.action'
      urllist=[]
      get_news_list(url)
main()
