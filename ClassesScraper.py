import re
import certifi
import ssl
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


try:
    url = "https://classes.usc.edu/term-20231/classes/csci/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    
except HTTPError as e:
    print("An HTTP Error occurred while accessing the URL ", url, ". See below for details: \n", e.code)

except URLError as e:
    print("The URL is invalid or not accessible. See below for details: \n", e.code)

else:
    soup = BeautifulSoup(html, "html.parser")
    classes = soup.find_all("div", { "class": "course-info expandable" })
    lst = []
    pattern = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

    for c in classes:
        instr = c.find("td", {"class": "instructor"})
        instrLink = instr.find("a")
        if instrLink:
            try:
                req = Request(url = instrLink["href"], headers = headers) 
                html1 = urlopen(req, context = ssl.create_default_context(cafile=certifi.where())).read() 
            except: 
                emails = []
            else:
                soup1 = BeautifulSoup(html1, "html.parser")
                emails = pattern.findall(soup1.text)

        #Code, Name, Description, Instructor
        lst.append((c["id"], 
        c.find("a").contents[-2], 
        c.find("div", {"class": "catalogue"}).contents[0],
        instr.text,
        emails))
    
    with open("ClassesInfo.csv", "w", newline = "\n") as myfile:
        wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
        for tup in lst:
            wr.writerow(tup)
    
    