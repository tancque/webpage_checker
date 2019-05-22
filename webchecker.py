# Website checker v1.1
#
# mvdl 02-02-2019

# Update v1.1

# added support for manual added test_strings without position test.
#       you can now manual add test_strings and website ; delimited in the conf-file with offset 0.
#       strings with offset 0 are not tested on position, only on occurence.

# Cleanup and standarized name
#       replaced dutch comments with english
#       Configfile class renamed to WebChecker

# requires beautifulsoup. Install pip install beautifulsoup4

import urllib.request
import random
import sys
from bs4 import BeautifulSoup


print ("start program")

class WebChecker:
        
        #main class
        # variables :
        # ipath = location configfile
        # clines = list with configfile lines
        # body = html string body of webpage requested
        # methods:
        # extract_test_string : extract teststring from website without teststring in conffigfile
        # load_page : load and extract html body from url
        # test_string: test if string is in body of webpage
        # check_lines: iterate configfile lines
        # end_object: write up any changes to conffigfile
        
        

        def __init__(self, path):
                self.ipath = path
                FILE = open(path, "r")
                self.clines = FILE.read().split("\n")
                FILE.close()

        def extract_test_string(self, Confline):
                # open website en extract a string of 50 chars
                # at random position between <Body> tags
                # add test_string and postition colon delimited
                # to the conf file

                # download web page
                
                self.load_page(Confline)
                start = random.randint(1,len(self.body)-50)
                new_string = self.body[start:start+50].replace("\n","")
                print ("test_string extracted : " + new_string)
        

                # write test_string and startposition to conf file
                newlines = list()
                for line in self.clines:
                        if Confline in line:
                                newline=Confline + ";" + str(start) + ";" + new_string
                        else:
                                newline = line
                        newlines.append(newline)

                self.clines = newlines
                

        def load_page(self, URL):
                # Load page and return body

                try:
                        response = urllib.request.urlopen(URL)
                        html = response.read().decode("utf-8")
                        soup = BeautifulSoup(html,features="html.parser")
                        self.body = str(soup.body)
                        
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
                

        def test_string(self, Confline):

                # openwebsite en extract test_string. compare with parsed data
                testData = Confline.split(";")
                self.load_page(testData[0])

                if (testData[1] == 0):
                        # 0 offset, no positional check
                        newString =  self.body.replace("\n","")
                        if newString not in testData[2]:
                                print("!!! Site changed, string not found: " + testData[0])
                                print("!!! registered test_string == " + testData[2])
                        else:
                                print("+++ site ok : " + testData[0])
                                
                else:

                
                        startpos = int(testData[1])
                        newString =  self.body[startpos:startpos+50].replace("\n","")
                        if  newString != testData[2]:
                                print("!!! Site changed: " + testData[0])
                                print("!!! registered test_string == " + testData[2])
                                print("!!! found string == " + newString)
                        else:
                                print("+++ site ok : " + testData[0])
                
                
        
        def check_lines(self):
                for Confline in self.clines:
                        print (Confline)
                        Confline = Confline.replace("\n","")
                        if (';' not in Confline) and (bool (Confline)):
                                Checker.extract_test_string(Confline)
                        elif (bool (Confline)):
                                Checker.test_string(Confline)
        
        def end_object(self):
                print ("closing conffile")
                FILEW = open(self.ipath, "w")
                for line in self.clines:
                        FILEW.write(line+"\n")
                FILEW.close()


if not sys.argv[1]:
        print ("reference to configfile not found")
        print ("usage : python WebChecker.py <path to configfile>")
        exit(4)
        
                                
# Conffile = Configfile("d:\dev\pyprojects\websites.conf")
Checker = WebChecker(sys.argv[1])
print ("configfile read, starting check")
Checker.check_lines()
print("ending it all...")               
Checker.end_object()





