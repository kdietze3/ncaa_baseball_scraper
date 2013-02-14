import re
import httplib
from bs4 import BeautifulSoup


connection = httplib.HTTPConnection("www.d1baseball.com")
connection.request("GET", "/2013/daily/0215.htm")
response = connection.getresponse()
xml = response.read()

soup = BeautifulSoup(xml)

##print(soup.prettify())


##Deemed not effective due to additional game location notes only present in some games.
##conferenceArray = re.findall(r'<h4><center><b><a\sname=.+?</td></tr></table></td>\s+</tr></table>',xml,re.DOTALL)
##
##for i in range(0,len(conferenceArray)):
##    conferenceArray[i] = re.sub(r'<.*?>',"",conferenceArray[i])
##    conferenceArray[i] = re.sub(r'\s\s+',"\n",conferenceArray[i])
##    conferenceArray[i] = re.split('\n|\t',conferenceArray[i])

##Just finds first table
table = soup.find('table')

rows = table.findAll('tr')
data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
data = [[u"".join(d).strip() for d in l] for l in data]
    
