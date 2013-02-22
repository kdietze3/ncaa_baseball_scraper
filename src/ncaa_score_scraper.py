import httplib
from bs4 import BeautifulSoup
from boto import *
import datetime
import time

def upload(date,league):
    ##Upload to Amazon Web Services
    s3 = connect_s3()
    bucket = s3.create_bucket('ncaa_baseball_data')  # bucket names must be unique
    key = bucket.new_key('2013/'+league+'/'+date+'.txt')
    key.set_contents_from_filename("./" + date+"-" + league + ".txt")
    key.set_acl('public-read')

def scrape(month, day):
    date = month+day
    
    connection = httplib.HTTPConnection("www.d1baseball.com")
    connection.request("GET", "/2013/daily/" + date + ".htm")
    response = connection.getresponse()
    xml = response.read()

    soup = BeautifulSoup(xml)

    leagues = ["ranked", "ameast", "a10", "acc", "atlsun", "big10", "big12", "bigeast", "bigsouth", "bigwest", "colonial", "cusa", "div1indy", "greatwest", "horizon", "maac", "mac", "meac", "mvc", "mwc", "nec", "ovc", "pac12", "patriot", "sec", "socon", "southland", "swac", "summit", "sunbelt", "wcc", "wac"]

    print "Leagues: "+str(len(leagues))
    

    # #Just finds first table
    tables = soup.findAll('table')
    tableArray = []
    final = []
    data = []
    
    for table in tables:
        if len(table) == 1:
            tableArray.append(table)
   
    
    ##tables = soup.findAll('table')
    
    for i in range(0,len(tableArray)):
        data.append(None)
    
    for i in range(0,len(tableArray)):
        rows = tableArray[i].findAll('tr')
        temp = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        data[i] = [[u"".join(d).strip() for d in l] for l in temp]
    
        
    if(len(data)!= 32):
        start = 1
    else:
        start = 0    
    
    
    for j in range(start,len(data)):
        f = open(date +"-"+leagues[j]+ ".txt", 'w')
        f.write("")
        f.close()

        f = open(date +"-"+leagues[j]+ ".txt", 'a')
        
        if(j != 0):
            for k in range(0, len(data[j]),13):    
                for i in range(1, len(data[j][k]), 9):
                    f.write(data[j][k][i] + "," + data[j][k][i + 1] + "," + data[j][k][i + 2] + "," + data[j][k][i + 3] + "," + data[j][k][i + 6] + "\n")
            f.close()
            print "League: " + leagues[j] + " Date: " + date + " COMPLETED"
            upload(date, leagues[j])
        else:
            for i in range(1, len(data[j][0]), 9):
                f.write(data[j][0][i] + "," + data[j][0][i + 1] + "," + data[j][0][i + 2] + "," + data[j][0][i + 3] + "," + data[j][0][i + 6] + "\n")
            f.close()
            print "League: " + leagues[0] + " Date: " + date + " COMPLETED"
            ##Upload to Amazon Web Services
            upload(date,leagues[0])
    
def convertTo2DigitString(num):
    if num < 10:
        return "0"+str(num)
    else:
        return str(num)   

def updateWholeSeason():
    for j in range(2,6):
        startDay = 1
        if j == 1:
            numDays = 31
        elif j == 2:
            numDays = 28
            startDay = 15
        elif j == 3:
            numDays = 31
        elif j == 4:
            numDays = 30
        elif j == 5:
            numDays = 31
        else:
            numDays = 0
        month = convertTo2DigitString(j)
        for i in range(1,numDays+1):
            day = convertTo2DigitString(i)
            scrape(month,day)

def runForCurrentDayWithUpdates():
    while(1):
        now = datetime.datetime.now()

        currentDay = now.day
        currentMonth = now.month
        currentHour = now.hour

        print "Hour: "+str(currentHour)
        print "Month: "+str(currentMonth)
        print "Day: " + str(currentDay)
    
        if currentHour >= 12:
            month = convertTo2DigitString(currentMonth)
            day = convertTo2DigitString(currentDay)
            scrape(month,day)
    
        time.sleep(3000)  # Delay for 1 minute (60 seconds)





        

##scrape("02","15")





