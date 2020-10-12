import Library
from urllib.request import Request, urlopen
import discord
from googletrans import Translator
from html.parser import HTMLParser

HTML = []


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        HTML.append(data)
        return HTML


req = Request("https://www.worldometers.info/coronavirus/country/poland", headers={'User-Agent': 'Mozilla/5.0'})
webpage = str(urlopen(req).read())
parser = MyHTMLParser()
parser.feed(webpage)
HTML.remove('\\n')
print(HTML)
country = "usa"
language = str(Library.translator.translate(Library.exceptionCheck(country)[1], dest='pl'))
ind1 = language.find("text=") + 5
ind2 = language.find("pronunciation") - 2
language = language[ind1:ind2]
print(language)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
