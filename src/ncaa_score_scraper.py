import httplib
from bs4 import BeautifulSoup
from boto import *


day = "0215"

connection = httplib.HTTPConnection("www.d1baseball.com")
connection.request("GET", "/2013/daily/"+day+".htm")
response = connection.getresponse()
xml = response.read()

soup = BeautifulSoup(xml)

f = open(day+".txt", 'w')
f.write("")
f.close()


f = open(day+".txt", 'a')

##print(soup.prettify())


##Deemed not effective due to additional game location notes only present in some games.
##conferenceArray = re.findall(r'<h4><center><b><a\sname=.+?</td></tr></table></td>\s+</tr></table>',xml,re.DOTALL)
##
##for i in range(0,len(conferenceArray)):
##    conferenceArray[i] = re.sub(r'<.*?>',"",conferenceArray[i])
##    conferenceArray[i] = re.sub(r'\s\s+',"\n",conferenceArray[i])
##    conferenceArray[i] = re.split('\n|\t',conferenceArray[i])

##Just finds first table
table = soup.findAll('table')
gameArray = []
gameTable = []

rows = table[0].findAll('tr')
data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
data = [[u"".join(d).strip() for d in l] for l in data]

##Need 1,2,3,4,7
for i in range(1,len(data[0]),9):
   
    f.write(data[0][i]+"," +data[0][i+1]+"," +data[0][i+2]+"," +data[0][i+3]+"," +data[0][i+6]+"\n")
    
f.close()
