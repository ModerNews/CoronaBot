from urllib.request import Request, urlopen
import discord
import re
from googletrans import Translator
from html.parser import HTMLParser

translator = Translator()
HTML = []


class myHTMLParser(HTMLParser):
    notImportant = 0

    def handle_data(self, data):
        HTML.append(str(data))
        return HTML


def reset():
    HTML.clear()


def digital(sign):
    ret = False
    if 48 <= ord(sign) <= 57:
        ret = True
    return ret


def hasNumbers(inputString):
    return any(digital(char) for char in inputString)


def objectFinder(listHTML, index):
    ret = "N/A"
    leng = len(listHTML)
    for i in range(index + 1, (index + 4)):
        try:
            n = str(listHTML[i])
            if hasNumbers(n):
                ret = n
                break
        except:
            temp = 0
    return ret


def minusOjectFinder(listHTML, index):
    ret = "N/A"
    leng = len(listHTML)
    for i in range(index - 5, (index - 1)):
        try:
            n = str(listHTML[i])
            if hasNumbers(n) and n != 1:
                ret = n
                break
        except:
            temp = 0
    return ret


def findInList(list, value):
    for x in list:
        if x == value:
            return value
            break


def exceptionCheck(country):
    data = str(country)
    if data.lower() == "vatican":
        return ["Holy-see", "Watykan"]
    elif data.lower() == "usa":
        return ["us", "Stanów Zjednoczonych"]
    elif data.lower() == "poland":
        return ["poland", "Polska"]
    elif data.lower() == "uk" or data.lower() == "england" or data.lower() == "scotland" or data.lower() == "wales" or data.lower() == 'northern-ireland':
        return ["uk", "Wielka Brytania"]
    elif data.lower() == "el-salvador" or data.lower() == "el salvador":
        return ["el-salvador", "Salwador"]
    else:
        return [data, data]

def HttpsRead(url, country):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = str(urlopen(req).read())
    parser = myHTMLParser()
    parser.feed(webpage)

    try:
        HTML.remove('\\n')
    except:
        temp = 0

    try:
        ind1 = int(HTML.index(str(findInList(HTML, "Coronavirus Cases:"))))
        totalCases =objectFinder(HTML, ind1)
    except ValueError:
        totalCases = "N/A"

    try:
        ind1 = int(HTML.index(str(findInList(HTML, "Recovered:"))))
        cured = objectFinder(HTML, ind1)
    except ValueError:
        cured = "N/A"

    try:
        ind1 = int(HTML.index(str(findInList(HTML, "Deaths:"))))
        dead = objectFinder(HTML, ind1)
    except ValueError:
        dead = "N/A"

    try:
        activeCases = str(int(totalCases.replace(",", "")) - int(cured.replace(",", "")) - int(dead.replace(",", "")))
        if len(activeCases) > 3:
            n = -3
            activeCases = activeCases[:n] + ',' + activeCases[n:]
        if len(activeCases) > 7:
            n = -7
            activeCases = activeCases[:n] + ',' + activeCases[n:]
    except ValueError:
        activeCases = "N/A"

    try:
        ind1 = int(HTML.index(str(findInList(HTML, "Serious or Critical"))))
        critical = minusOjectFinder(HTML, ind1)
    except ValueError:
        critical = "N/A"

    newCases = "N/A"
    newDead = "N/A"
    if country == "świata":
        #new cases and deaths are made using data from table
        #label 1 - total cases
        #label 2 - New cases
        #label 3 - total deaths
        #label 4 - New deaths
        #label 5 - Total Recovered
        #label 6 - Active cases
        #label 7 - Critical
        #label 8 - cases for 1M
        #label 9 - deaths per 1M
        #label 10 - Total Tests
        #label 11 - Tests per 1M
        #label 12 - Population
        try:
            ind1 = int(HTML.index(str(findInList(HTML, "World"))))
            newCases = "N/A"
            newCases = objectFinder(HTML, ind1 + 3)
        except ValueError:
            newCases = "N/A"

        try:
            ind1 = int(HTML.index(str(findInList(HTML, "World"))))
            newDead = "N/A"
            newDead =objectFinder(HTML, ind1 + 7)
        except ValueError:
            newDead = "N/A"
    else:
        index = None
        try:
            index = int(HTML.index(str(findInList(HTML, "Latest News"))))
        except:
            newCases = "N/A"
            newDead = "N/A"
        try:
            for i in range(index + 1, index + 9):
                if str(HTML[i]).count("cases") >= 1 and hasNumbers(str(i)):
                    try:
                        newCases = str(HTML[i])
                        newCases = newCases.replace(" new cases", "")
                    except:
                        newCases = "N/A"
                elif str(HTML[i]).count("deaths") >= 1 and hasNumbers(str(i)):
                    try:
                        newDead = str(HTML[i])
                        newDead = newDead.replace(" new deaths", "")
                    except:
                        newCases = "N/A"
        except:
            newCases = "N/A"
            newDead = "N/A"
    temp1 = exceptionCheck(country)[1]
    language = str(translator.translate(temp1, dest='pl'))
    ind1 = language.find("text=") + 5
    ind2 = language.find("pronunciation") - 2
    language = language[ind1:ind2]

    embed = discord.Embed(title="Dane o chorobie", color=0xf00000)
    embed.set_author(name="Koronawirus dla " + language, url=url, icon_url="https://i.pinimg.com/564x/2b/87/3d"
                                                                            "/2b873d25cd30e703b1c7e7c2c2b567d8.jpg")
    embed.add_field(name="Wszystkie zarażenia", value=totalCases, inline=False)
    embed.add_field(name="Aktywne przypadki", value=activeCases, inline=True)
    embed.add_field(name="Śmierci", value=dead, inline=True)
    embed.add_field(name="W stanie krytycznym", value=critical, inline=True)
    embed.add_field(name="Zarażeni dzisiaj", value=newCases, inline=True)
    embed.add_field(name="Śmierci dzisiaj", value=newDead, inline=True)
    reset()
    return embed
