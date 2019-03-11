# Website checker v1
#
# mvdl 02-02-2019

# requires beautifulsoup. Install pip install beautifulsoup4

import urllib.request
import random
import sys
from bs4 import BeautifulSoup


print ("start program")

class Configfile:
        
        #all things concerning the list with urls en teststrings

        def __init__(self, path):
                self.ipath = path
                self.FILE = open(path, "r")
                self.clines = self.FILE.read().split("\n")
                self.FILE.close()

        def ExtractTestString(self, Confline):
                # open website en extract a string of 50 chars
                # at random position between <Body> tags
                # add teststring and postition colon delimited
                # to the conf file

                # download web page
                
                self.LoadPage(Confline)
                self.start = random.randint(1,len(self.body)-50)
                self.teststring = self.body[self.start:self.start+50].replace("\n","")
                print ("Teststring extracted : " + self.teststring)
        

                # write teststring and startposition to conf file
                self.newlines = list()
                for line in self.clines:
                        if Confline in line:
                                self.newline=Confline + ";" + str(self.start) + ";" + self.teststring
                        else:
                                self.newline = line
                        self.newlines.append(self.newline)

                self.clines = self.newlines
                

        def LoadPage(self, URL):
                # Load page and return body

                try:
                        self.response = urllib.request.urlopen(URL)
                        self.html = self.response.read().decode("utf-8")
                        self.soup = BeautifulSoup(self.html,features="html.parser")
                        self.body = str(self.soup.body)
                        
                except urllib.error.URLError:
                        print ("error in URL: " + Confline)
                        print ("skipping line in configfile")
                        exit(1)
                        
                except urllib.error.HTTPError:
                        print ("error in webserver response: " + Confline)
                        print ("skipping line in configfile")
                        exit(2)

                except socket.gaierror:
                        print ("site not found error" + Confline)
                        print ("skipping line in configfile")
                        exit(3)
                

        def TestString(self,Confline):

                # openwebsite en extract teststring. compare with parsed data
                self.testData = Confline.split(";")
                self.LoadPage(self.testData[0])

                # losse vars voor de substringpositie ivm problemen met dubbele haken en lijstreferentie
                self.startpos = int(self.testData[1])
                self.newString =  self.body[self.startpos:self.startpos+50].replace("\n","")
                if  self.newString != self.testData[2]:
                        print("!!! Site veranderd: " + self.testData[0])
                        print("!!! geregistreerde testsring == " + self.testData[2])
                        print("!!! gevonden antwoord == " + self.newString)
                else:
                        print("+++ site ok : " + self.testData[0])
                
                
        

        def EndObject(self):
                print ("closing conffile")
                self.FILEW = open(self.ipath, "w")
                for line in self.clines:
                        self.FILEW.write(line+"\n")
                self.FILEW.close()


if not sys.argv[1]:
        print ("reference to configfile not found")
        print ("usage : python webchecker.py <path to configfile>")
        exit(4)
        
                                
# Conffile = Configfile("d:\dev\pyprojects\websites.conf")
Conffile = Configfile(sys.argv[1])
print ("conffile gelezen")
for Confline in Conffile.clines:
        print (Confline)
        if (';' not in Confline) and (bool (Confline)):
                Conffile.ExtractTestString(Confline)
        elif Confline.replace("\n","") and (bool (Confline)):
                Conffile.TestString(Confline)
print("ending it all...")               
Conffile.EndObject()
