import requests
import zipfile
from io import BytesIO
from bs4 import BeautifulSoup
import os
import shutil

baseurl = "https://open.kattis.com/"
cookies = {'EduSiteCookie': '**INSERT COOKIE HERE****'}
username = "***INSERT USERNAME HERE***"



assignments = set()

def splitRow(row):
    cells = row.findChildren('td')
    returnlist = []
    for cell in cells:
        returnlist.append(cell.getText())
    return returnlist

def getAcceptedOnSite(url):
    get = requests.get(url,cookies=cookies)
    soup = BeautifulSoup(get.content, 'html.parser')
    table = soup.findChildren('table')
    rows = table[1].findChildren(['tr'])
    returnlist = []
    for row in rows[1:]:
        listRow = splitRow(row)
        if((listRow[2] not in assignments) and (listRow[3] == "Accepted")):
            assignments.add(listRow[2])
            returnlist.append(listRow)
    
    return returnlist

def getAllAccepted(username):
    toDownload = []
    for i in range(5000): #Assume no one has more than 5000 pages
        print("indexing page "+str(i))
        url = baseurl+"users/"+username+"?page="+str(i)
        resultFromPage = getAcceptedOnSite(url)
        if(len(resultFromPage) == 0):
            return toDownload
        toDownload = toDownload + resultFromPage    


def downloadContents(id,folder):
    try:
        os.mkdir(folder)
    except FileExistsError:
        print("Directory " , folder ,  " already exists,skipping")
        return
    url = baseurl+"submissions/"+str(id)+"/source"
    request = requests.get(url,cookies=cookies)
    zip_file = zipfile.ZipFile(BytesIO(request.content))
    for zip_info in zip_file.infolist():
        if zip_info.filename[-1] == '/':
            continue
        zip_info.filename = os.path.basename(zip_info.filename)
        zip_file.extract(zip_info,os.getcwd()+"/"+folder)

done = getAllAccepted(username)

for d in done:
    print("Downloading "+d[2])
    downloadContents(int(d[0]),d[2])

print("Finished!")
