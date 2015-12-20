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

def main():
    f   = open("nameResults.txt", 'a')
    tryNames(f)
    f.close()

if __name__ == "__main__":
    main()

