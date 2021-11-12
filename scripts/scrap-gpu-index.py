import sys
import os.path
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

URL = "https://www.gpucheck.com/nvidia-gpu-hierarchy-list-chart"
fname = ".cache/index.html"
sname = "index.html"
mname = "index.md"
content = ""

if not os.path.isdir(os.path.dirname(fname)):
    os.mkdir(os.path.dirname(fname))

if os.path.isfile(fname):
    with open(fname, "rb") as file:
        content = file.read()
else:
    page = requests.get(URL)
    content = page.content
    with open(fname, "wb") as file:
        file.write(content)

soup = BeautifulSoup(content, "html.parser")

title = soup.select("div.row div h1")[0]
description = title.find_next('div')
table = soup.select("div.row table")[0]

#print("#/bin/bash")
#for elem in table.find_all('a'):
#    print(elem.get('href').replace('/gpu/', 'python scripts/scrap-gpu.py '))
#exit()

content = '<link rel="stylesheet" type="text/css" media="screen" href="./css/combined.min.css" />\n' + \
          '<script src="./js/fontawesome-v5.7.0-all.js" ></script>\n' + \
          str(title) + '\n' + \
          str(description) + '\n' + \
          str(table).replace('/gpu/', './gpu/') + '\n'

with open(sname, "w") as file:
    file.write(content)

markdown = md(content.replace('\n', ''), heading_style='ATX').strip()
print(markdown)
with open(mname, "w") as file:
    file.write(markdown)
