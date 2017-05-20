import requests
import string
import time
from bs4 import BeautifulSoup

def tryNames(f):
    letters = "bcdfghjklmnpqrstvwxyz"
    numbers = "0123456789"
    alphnum = letters + numbers
    urlBase = "https://www.google.ca/search?q="
    #urlSpace= [w+x+y+z for w in letters for x in alphnum for y in alphnum for z in alphnum]
    urlSpace = [x for x in letters]

    for u in urlSpace:
        name = u
        tryName = True
        print("Processing " + name + "...")

        while tryName:
            try:
                url     = urlBase + name
                r       = requests.get(url)

                soup    = BeautifulSoup(r.content, "html.parser")
                resultStats = soup.find_all("div", {"id":"resultStats"})

                result  = resultStats[0].text

                words   = result.split()
                numInd  = 1     # the google string is "About N results" so "N" is at index 1
                if result[0].isnumeric():
                    numInd = 0
                strRep = "".join([c for c in words[numInd] if c != ','])    # remove commas
                f.write(name + ": " + strRep + '\n')

                print(name + ": " + strRep + '\n')
                time.sleep(1)   # delay for one second
                tryName = False
            except:
                print("Google services failed on " + name + ". Trying again.")

def saveNamesToFile(fileName):
    f   = open(fileName, 'a')
    tryNames(f)
    f.close()

def processNames(fileName, show):
    results = []
    with open(fileName, 'r') as f:
        for line in f:
            strList = line.split()
            results.append((strList[0], int(strList[1])))
    results = sorted(results, key = lambda name: name[1])
    for i in range(show):
        print(results[i][0], results[i][1])


def main():
    fileName = "moreNameResults.txt"
    saveNamesToFile(fileName)
#    processNames(fileName, 5)

if __name__ == "__main__":
    main()
