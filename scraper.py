import bs4 as bs
import urllib.request
import re
import csv

def getTds(fromStn, toStn):
    print('scraping:' + fromStn+ "/" + toStn )
    sauce = urllib.request.urlopen('http://ojp.nationalrail.co.uk/service/timesandfares/' +fromStn+'/'+toStn+ '/today/1130/dep').read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    tds = soup.find_all('td', {"class" : "dur"})
    return tds

def getDuration(tds):

    mins = 0
    hrs = 0
    if not tds:
        tds = ["0h","0m"]
    t = tds[0].text
    time = re.sub('[\s+]', '', t)

    if time.find('h') > 0:
        hrs = time.split('h')
        if hrs[1].find('m'):
            mins = hrs[1].split('m')
            mins = mins[0]
        hrs = hrs[0]
    else:
        if time.find('m'):
            mins = time.split('m')
            mins = mins[0]
    mins = int(hrs) * 60 + int(mins)
    return mins

#print(getDuration(getTds("ABW","AVY")))

def getStationDict():
    with open('station_codes.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    return mydict

stations = getStationDict()

#print(stations["AVY"])
keys = stations.keys()

def getAllDurations(CRS_codes):
    durations = []
    for fromStn in CRS_codes.keys():
        for toStn in CRS_codes[fromStn]:
            if fromStn != toStn:
              time = (getDuration(getTds(fromStn, toStn)))
              entry = (fromStn, toStn, time)
              durations.append(entry)
              #print(entry)
    return durations

def toCSV(filename, durations):
    with open(filename, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['From', 'to', 'duration'])
        for row in durations:
            print(row)
            csv_out.writerow(row)


#print(getAllDurations(keys))
stn = {}
stn['LUT'] = ['KGX', 'BDM', 'NMP', 'LVC', 'GLC']
stn['KGX'] = ['SOU', 'GTW', 'POO', 'MAN', 'LUT']
stn['LVC'] = ['LVC', 'MAN', 'KGX']
stn['SOU'] = ['KGX', 'POO']
stn['POO'] = ['KGX', 'SOU']

durations = getAllDurations(stn)
toCSV('durations.csv', durations)