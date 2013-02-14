import re
import httplib
from collections import namedtuple



connection = httplib.HTTPConnection("www.d1baseball.com")
connection.request("GET", "/2013/daily/0215.htm")
response = connection.getresponse()
xml = response.read()

conferenceArray = re.findall(r'<h4><center><b><a\sname=.+?</td></tr></table></td>\s+</tr></table>',xml,re.DOTALL)

for i in range(0,len(conferenceArray)):
    conferenceArray[i] = re.sub(r'<.*?>',"",conferenceArray[i])
    conferenceArray[i] = re.sub(r'\s\s+',"\n",conferenceArray[i])
    conferenceArray[i] = conferenceArray[i].split(r'\n')

##for i in range(0,len(conferenceArray)):
##    for j in range(0,conferenceArray[i]):
##        gameArray[j,0]
        
