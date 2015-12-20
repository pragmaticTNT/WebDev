import requests
import string
from bs4 import BeautifulSoup

lower   = string.ascii_lowercase
urlBase = "https://www.google.ca/search?num=100&newwindow=1&safe=off&site=webhp&q="
urlSpace= [x for x in lower[:20:-1] for y in lower for z in lower]
#urlSpace= ["abc", "bcd"]
resultList = []

for u in urlSpace:
    #name    = u + u[::-1]
    name     = u
    print("Processing " + name + "...")
    url     = urlBase + name
    r       = requests.get(url)

    soup    = BeautifulSoup(r.content, "html.parser")
    resultStats = soup.find_all("div", {"id":"resultStats"})

    print(r.content)
    result  = resultStats[0].text
    #print("name: " + name + " result: " + result)

    temp    = result.split()
    val     = 1
    if result[0].isnumeric():
        val = 0

    try:
        strRep = "".join([c for c in temp[val] if c != ','])
        resultList.append((name, int(strRep)))
    except:
        pass

finalList = sorted(resultList, key = lambda item: item[1])
print(finalList)
