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

# Update v1,2
# added emailsupport.
#       mail can be send via an smtp emailserver 
#       to config an emailserver use a line in the conffile with following syntax:
#       smtp:smtpservername:mailfrom:mailto;mailto;mailto;etc;etc;

# requires beautifulsoup. Install "pip install beautifulsoup4


import urllib.request
import random
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
                self.mail_body = "Results of webchecker<BR><BR>"
                FILE.close()
                self.mail_server = 'none'

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
                self.mail_body += "<BR> test_string extracted : " + new_string 
        

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
                        
                except Exception as e: 
                        print ("error in URL: " + URL + ", " + str(e))
                        print ("skipping line in configfile")
                        self.mail_body += "<BR> error in URL: " + URL + ", " + str(e)
                        self.body = ""
                      

        def test_string(self, Confline):
        
                # openwebsite en extract test_string. compare with parsed data
                testData = Confline.split(";")
                self.load_page(testData[0])
                if (len(self.body) > 0):
                        if (testData[1] == "0"):
                                # 0 offset, no positional check
                                newString =  self.body.replace("\n","")
                                if testData[2] not in newString:
                                        print("!!! Site changed, string not found: " + testData[0])
                                        print("!!! registered 0 test_string == " + testData[2])
                                        self.mail_body += "<BR> site changed " + testData[0]
                                                                               
                                else:
                                        print("+++ site ok : " + testData[0])
                                        self.mail_body += "<BR> +++ site ok : " + testData[0]
                        else:
        
                        
                                startpos = int(testData[1])
                                newString =  self.body[startpos:startpos+50].replace("\n","")
                                if  newString != testData[2]:
                                        print("!!! Site changed: " + testData[0])
                                        print("!!! registered test_string == " + testData[2])
                                        print("!!! found string == " + newString)
                                        self.mail_body += "<BR> site changed " + testData[0]
                                else:
                                        print("+++ site ok : " + testData[0])
                                        self.mail_body += "<BR> +++ site ok : " + testData[0]
                        
        
        def check_lines(self):
                for Confline in self.clines:
                        print (Confline)
                        Confline = Confline.replace("\n","") #remove superfloues line endings
                        # print ('debug : '+ Confline[:3])
                        if (Confline[:4] == 'smtp'):
                                # smtp configline gedetecteerd
                                print ('debug mailserver configline detected')
                                self.config_email(Confline)
                        elif (';' not in Confline) and (bool (Confline)):
                                self.extract_test_string(Confline)
                        elif (bool (Confline)):
                                self.test_string(Confline)

        def config_email(self, confline):
                
                data = confline.split(";")
                self.mail_server = data[1]
                self.mail_from = data[2]
                self.mail_to = data[2:]

                print ('config mailsettings : mailserver = ' + self.mail_server)
                print ('config mailsettings : to = ' +  ", ".join(self.mail_to))
                

        def send_email(self):

                mail_object = MIMEMultipart('alternative')
                mail_object['Subject'] = "webpage checker"
                mail_object['From'] = self.mail_from
                mail_object['To'] = ", ".join(self.mail_to)

                self.mail_body += "<P> --- end automated message --- </HTML></BODY>"
                mime_mail_body = MIMEText (self.mail_body, 'html')
                mail_object.attach(mime_mail_body)
                mail_server = smtplib.SMTP(self.mail_server)
                mail_server.sendmail(self.mail_from, self.mail_to, mail_object.as_string())  
                mail_server.quit
                
                
        
        
        def end_object(self):
                print ("closing conffile")
                FILEW = open(self.ipath, "w")
              
                for line in self.clines:
                        line  = line.strip()
                        if len(line) > 0:
                                FILEW.write(line+"\n")
                FILEW.close()
                if (self.mail_server != 'none'):
                        print ('sending email')
                        self.send_email()                    
                


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





