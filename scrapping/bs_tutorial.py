import requests
import string
from bs4 import BeautifulSoup

def tryNames(f):
    letters = "bcdfghjklmnpqrstvwxyz"
    urlBase = "https://www.google.ca/search?q="
    urlSpace= [x+y for x in letters for y in letters]

    for u in urlSpace:
        name    = "xyl" + u
        print("Processing " + name + "...")

        try:
            url     = urlBase + name
            r       = requests.get(url)

            soup    = BeautifulSoup(r.content, "html.parser")
            resultStats = soup.find_all("div", {"id":"resultStats"})

            result  = resultStats[0].text

            temp    = result.split()
            val     = 1
            if result[0].isnumeric():
                val = 0

            strRep = "".join([c for c in temp[val] if c != ','])
            f.write(name + ": " + strRep + '\n')
        except:
            print("Google services failed on " + name)
            break

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
    fileName = "nameResults.txt"
#   saveNamesToFile(fileName)
    processNames(fileName, 5)

if __name__ == "__main__":
    main()

