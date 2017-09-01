import bs4 as bs
import urllib.request, re, csv, os.path

stn = {}
stn['LUT'] = ['KGX', 'BDM', 'NMP', 'LVC', 'GLC']
stn['KGX'] = ['SOU', 'GTW', 'POO', 'MAN', 'LUT']
stn['LVC'] = ['LVC', 'MAN', 'KGX']
stn['SOU'] = ['KGX', 'POO']
stn['POO'] = ['KGX', 'SOU']

# The train site we are scraping
URL = 'http://ojp.nationalrail.co.uk/service/timesandfares/'
# The end parameters for te URL : day/time/direction
END = '/today/1130/dep'

def getTds(fromStn, toStn):
    '''Get the td tags'''

    print('scraping:' + fromStn+ "/" + toStn )
    sauce = urllib.request.urlopen(URL + fromStn + '/' + toStn + END).read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    tds = soup.find_all('td', {"class" : "dur"})
    return tds

def getDuration(tds):
    '''Get the duration information from td tags'''

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


def getStationDict(file_name):
    '''create a dictionary from the station_codes .csv file'''

    if not os.path.isfile(file_name):
        return stn
    with open(file_name, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
    return mydict


def getAllDurations(CRS_codes):
    '''Get the duration for the CRS codes'''

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
    '''Save the data into a csv file'''

    with open(filename, 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['From', 'to', 'duration'])
        for row in durations:
            print(row)
            csv_out.writerow(row)

if __name__ == "__main__":
    durations = getAllDurations(getStationDict('station_codes.csv'))
    toCSV('durations.csv', durations)