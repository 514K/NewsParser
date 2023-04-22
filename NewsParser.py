from bs4 import BeautifulSoup
import os
import sys
import requests


class InvalidSettings(Exception):
    def __init__(self, text):
        self.txt = "Check conf: " + text


class NewsParser:
    __formatSettings = {
        # (int) Максимальное количество символов в строке
        "MaxWidthText": "80",
        # (str) s - текст ссылки, l - сама ссылка ["[{s};{l}]", "{s}[{l}]", "[{l};{s}]"]
        "LinksFormat": "[{s};{l}]",
        # (int) Количество отступов для заголовка статьи
        "NumTitleIndents": "2",
        # (int) Количество отступов для параграфов
        "NumParagraphIndents": "1",  
    }

    __parseSettings = {
        # (str) Откуда получать ссылки ["cmd", "file"]
        "LinksHolder": "cmd",  
        # (str) Имя файла (задается если LinksHolder == file)
        "FileHolderName": "None",
        # (bool) Если истина, то парсит все заданные сайты, иначе только первый
        "MultiURLs": "False",
        # (str) Тег для остановки поиска текста статьи
        "StopClass" : "footer",
        # (str) Тег для поиска спам вставок 
        "SpamTag" : "a",
        # (str) Тег для поиска параграфов
        "FindTag" : "p",
        # (str) Ищет параграфы по классу (работает только если FindTag == None или по FindTag не найдено элементов)
        "FindClass" : "None"
    }

    def __init__(self):
        pass

    def setSettings(self, formatSettings, parseSettings):
        with open(formatSettings, "r") as file:
            for line in file:
                sett = line.split("=")
                self.__formatSettings.update(
                    [(sett[0], sett[1].replace("\n", ""))])

        with open(parseSettings, "r") as file:
            for line in file:
                sett = line.split("=")
                self.__parseSettings.update(
                    [(sett[0], sett[1].replace("\n", ""))])

    def parse(self):
        if self.__parseSettings["LinksHolder"] == "cmd":
            if self.__parseSettings["MultiURLs"] == "False":
                self.__singleParse(sys.argv[1])
            else:
                self.__multiParse(sys.argv[1:])

        elif self.__parseSettings["LinksHolder"] == "file":
            if self.__parseSettings["FileHolderName"] != "None":
                with open(self.__parseSettings["FileHolderName"]) as file:
                    self.__multiParse(file.readlines())
            else:
                raise InvalidSettings("FileHolderName")
        else:
            raise InvalidSettings("LinksHolder")

    def __singleParse(self, url):
        domain = url[:url.index("/")] if url.find("www") == 0 else url[:url.index("/", 8)]
        site = requests.get(url)

        totalText = ""

        soup = BeautifulSoup(site.text, 'lxml')

        totalText += soup.find("h1").text.lstrip().rstrip().replace("\n", "") + (int(self.__formatSettings["NumTitleIndents"]) + 1) * "\n"

        maxSymbsInLine = int(self.__formatSettings["MaxWidthText"])
        paragraphIndents = int(self.__formatSettings["NumParagraphIndents"])
        linkMask = self.__formatSettings["LinksFormat"]
        stopClass = self.__parseSettings["StopClass"]
        spamTag = self.__parseSettings["SpamTag"]
        FindTag = self.__parseSettings["FindTag"]
        FindClass = self.__parseSettings["FindClass"]
        
        elements = []
        if len(soup.find_all(FindTag)) > 0 and FindTag != "None":
            elements = soup.find_all(FindTag)
        else:
            elements = soup.find_all(class_=FindClass)

        for item in elements:
            footerOrSpamLinkIsFind = False
            for parent in item.parents:
                if str(parent.get("class")).lower().find(stopClass) != -1:
                    footerOrSpamLinkIsFind = True
            if len(item.find_parents(spamTag)) > 0:
                footerOrSpamLinkIsFind = True

            if footerOrSpamLinkIsFind:
                break

            if item.text == "\n":
                continue

            tmp = str(item)
            for link in item.find_all("a"):
                href = str(link.get("href"))
                
                if href.find("/") == 0:
                    href = domain + href

                tmp = tmp.replace(str(link), linkMask.format(s = link.text, l = href))

            tmp = BeautifulSoup(tmp, 'lxml').text

            if len(tmp) > maxSymbsInLine:
                linesList = []
                wordList = tmp.split(" ")
                tmpLine = ""
                for word in wordList:
                    if len(tmpLine + word) > maxSymbsInLine:
                        linesList.append(tmpLine + "\n")
                        tmpLine = ""
                    tmpLine += word + " "
                linesList.append(tmpLine + "\n")
                
                for line in linesList:
                    totalText += line
                
                totalText += paragraphIndents * "\n"
            else:
                totalText += tmp + paragraphIndents * "\n"
        
        self.__saveResult(url, totalText)

    def __multiParse(self, urls):
        for url in urls:
            self.__singleParse(url.replace("\n", ""))

    def __saveResult(self, url, totalText):
        urlWuthoutProtocol = url[url.index("//") + 2:]
        dirs = urlWuthoutProtocol.split("/")
        pageName = dirs[len(dirs) - 1]
        dirs.remove(pageName)

        pageNameWithoutExt = ".".join(pageName.split(".")[:-1])

        pageDir = "pages/" + "/".join(dirs)

        if not os.path.isdir(pageDir):
            os.makedirs(pageDir)


        with open("{}/{}.txt".format(pageDir, pageNameWithoutExt), "w", encoding="utf8") as file:
            file.write(totalText)
