'''
 Megaupload resolver (uses functions from _megaupload)
'''
import filehostmodule
from _megaupload import *

class MegapornModule(filehostmodule.FileHostModule):
    
    def __init__(self):
        self.username=""
        self.password=""
        self.baseurl=regular

    def getIconFileHost(self):
        return os.path.join(__file__, "resolver_icons", "megaupload.png")
    
    def getRegularExpression(self):
        return r"http://(www.)?hotfile\.com/dl/\d+/[0-9a-zA-Z]+/"
    
    def filterOnlineURLs(self, urls):
        validurls = self.filterValidURLs(urls)
        return self.__checkHFLinks(self.username,self.password,validurls)

    def isLoginValid(self, username, password):
        return not a==".invalid username or password"

    def isLoginForStreaming(self, username, password):
        return self.__hotfileapicall("getuserinfo",username,password,[]).find("is_premium=1")>-1
    
    def login(self, username, password):
        self.username=username
        self.password=password
        return self.isLoginValid(username, password)

    def isLoggedIn(self):
        return self.isLoginValid(self.username, self.password)
    
    def logout(self):
        self.username=""
        self.password=""
        return True

    def resolveURLs(self, urls):
        res=self.__getHFLinks(self.username,self.password,urls)
        ret=[]
        resa=res.split("\n")
        for line in resa:
            try:
                cols=line.split("|")
                if cols[0]!="":
                    if cols[1][0:4]=="http":
                        ret.append(cols[1])
            except:
                pass
        return ret

    def getFileName(self, url):
        res=self.__getHFLinks(self.username,self.password,[url])
        cols=res.replace("\n","").split("|")
        try:
            if cols[0]!="":
                if cols[1][0:4]=="http":
                    return cols[0]
        except:
            pass
        return None
