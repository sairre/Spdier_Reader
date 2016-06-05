# -*- coding: utf-8 -*-
import urllib2
import re
import os
import thread
import time
class HTML_Tool:
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    EndCharToNoneRex = re.compile("<.*?>")
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")
    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," "),("\"nbsp;"," ")]

    def Replace_Char(self,x):  
        x = self.BgnCharToNoneRex.sub("",x)  
        x = self.BgnPartRex.sub("\n    ",x)  
        x = self.CharToNewLineRex.sub("\n",x)  
        x = self.CharToNextTabRex.sub("\t",x)  
        x = self.EndCharToNoneRex.sub("",x)  
  
        for t in self.replaceTab:    
            x = x.replace(t[0],t[1])    
        return x


def getpage(index,mydir,page):
    newpage = page[0].replace("\"","")
    urls = index+newpage
   # print urls
    filename =  page[1].replace("*","x").replace("?","x")
    if os.path.exists("D:\\"+mydir+"\\"+filename.decode("gbk")+".txt"):
    #    print "exist and skip"
        return
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(urls,headers = headers)
    response = urllib2.urlopen(req)
    #response = urllib2.urlopen(urls,timeout = 5)
    html = response.read()
    
    item = re.findall("<div id=(.*?)>&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</div>",html)
    mytool = HTML_Tool()
    if os.path.exists("D:\\"+mydir+"\\"+filename.decode("gbk")+".txt"):
        print "skip"
    else:
        #print type(page[1])
        print filename.decode("gbk")
        
        f = open('D:\\'+mydir+'\\'+ filename.decode("gbk")+'.txt','a')
        f.write("\n\t")
       
    
      #  print filename.decode("gbk")
        for it in item:
            da = mytool.Replace_Char(it[1])
            f.write(da)
            #print da
        f.close()



def downloadfiles(infos,index,mydir):
    for page in infos:
        try:
            getpage(index,mydir,page)
        except Exception,e:
            print Exception,":",e
    thread.exit_thread()
    print "DONE THE THREAD>>>"

#myUrl = 'http://www.biquge.la/book/11032'
myUrl = "https://www.biquku.com/0/302/"
#myUrl = 'http://www.23wx.com/html/0/298/'
mydir = u"武神空间"
#mydir = u"斗破苍穹"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request(myUrl,headers = headers)
#mainresponse = urllib2.urlopen(req)
mainresponse = urllib2.urlopen(myUrl)
maininfo = mainresponse.read()
pageinfos = re.findall("<a href=(.*?)>(.*?)</a>",maininfo)


print "+++++++++++++++++++++++++++++++++++++++++++++++"
index = 0
lens = len(pageinfos)
for cnt in range(lens):
    check_page = pageinfos[index]
    filename =  check_page[1].replace("*","x").replace("?","x")
    if os.path.exists("D:\\\\"+mydir+"\\\\"+filename.decode("gbk")+".txt"):
        strpath = "D:\\"+mydir+"\\"+filename.decode("gbk")+".txt"
        pageinfos.remove(check_page)
    else:
       # print "XD:\\"+mydir+"\\"+filename.decode("gbk")+".txt"
        index = index + 1

print "check over"
print len(pageinfos)

threads = 10
start =0;
end = len(pageinfos)/threads

for i in range(threads):
    tmpinfo = pageinfos[start:end]
    start = end+1
    end = end + len(pageinfos)/threads
    try:
        thread.start_new_thread(downloadfiles,(tmpinfo,myUrl,mydir))
    except Exception,e:
        print Exception,":",e

print "-----------------------------------------------"

    
