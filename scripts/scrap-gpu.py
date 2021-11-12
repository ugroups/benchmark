import sys
import os.path
import requests
from bs4 import BeautifulSoup
#from markdownify import markdownify as md

BASE_URL = "https://www.gpucheck.com"
URL = "https://www.gpucheck.com/gpu/nvidia-geforce-rtx-3090"
BASE_ROOT = ".."
if len(sys.argv) > 1:
    URL = sys.argv[1]
    if not URL.startswith(BASE_URL):
        URL = BASE_URL + '/gpu/' + URL
slug = URL.split('/')[4]
fname = '.cache/' + slug + ".html"
sname = 'gpu/' + slug + ".html"
#mname = 'gpu/' + slug + ".md"
content = ""

if not os.path.isdir(os.path.dirname(sname)):
    os.mkdir(os.path.dirname(sname))

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
print(title.text)

description = soup.select("div.row div p")[0]
for elem in description.find_all('a'): elem.decompose()
print(description.text)

img = soup.select("div.row div.row img")[0]
img_src = BASE_URL + img.get('src')
img_html = str(img)
img_html = img_html.replace('w-100', 'w-25')
#img_html = img_html.replace('src="', 'src="' + BASE_URL)
img_html = img_html.replace('src="/static', 'src="' + BASE_ROOT)
print(img_src)

img_fname = img.get('src').replace('/static', '.')
if not os.path.isdir(os.path.dirname(img_fname)):
    os.mkdir(os.path.dirname(img_fname))
if not os.path.isfile(img_fname):
    img_content = requests.get(img_src).content
    with open(img_fname, "wb") as file:
        file.write(img_content)

summary = soup.find("div", id="summary")
for elem in summary.find_all('a'): elem.decompose()
for elem in summary.find_all('small'): elem.decompose()
summary.find('div', id="exampleModal").decompose()

spec_h4 = soup.find("h4", id="specifications")
spec_div = spec_h4.find_next("div")

with open(sname, "w") as file:
    file.write('<link rel="stylesheet" type="text/css" media="screen" href="' + BASE_ROOT + '/css/combined.min.css" />\n')
    file.write('<script src="' + BASE_ROOT + '/js/fontawesome-v5.7.0-all.js" ></script>\n')
    file.write('<div class="row">\n')
    file.write(img_html + '\n')
    file.write('<div class="w-75">\n')
    file.write(str(title) + '\n')
    file.write(str(description) + '\n')
    file.write('</div>\n')
    file.write('</div>\n')
    file.write(str(summary) + '\n')
    file.write(str(spec_h4) + '\n')
    file.write(str(spec_div) + '\n')

#markdown = md(str(summary), strip=['small']).strip()
#print(markdown)
#with open(mname, "w") as file:
#    file.write(markdown)
