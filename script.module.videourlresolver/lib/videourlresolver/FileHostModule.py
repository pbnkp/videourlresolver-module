import os
import re
import urllib
import traceback
        
class FileHostModule:
    """
    Generic FileHostModule for resolving and checking links for file hosts within XBMC addons
    """
    def getIconFileHost(self):
        """
        Returns a URL with an icon for the filehost.
        """
        return "default.png"
    
    def getIconURL(self, url):
        """
        Returns a URL with an icon for the specified URL
        """
        return self.getIconFileHost()
    
    def getRegularExpression(self):
        """
        Returns a regular expression that finds links of this file host within HTML source.
        """
        print "FileHostModule.py: Default regular expression returned from FileHostModule interface. Please override this method!"
        return r"((https?|ftp|gopher|telnet|file|notes|ms-help):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)" #matches all valid http/https/ftp urls
    
    def isValidLink(self, url):
        """
        Checks if the supplied link is valid for this file host
        """
        try:
            return (len(self.filterValidURLs([url]))>0)
        except:
            return false
    
    def filterValidURLs(self,urls):
        """
        Checks if the supplied links are valid for this file host
        """
        res=[]
        for url in urls:
            if re.findall(self.getRegularExpression(),url)!=None:
                res.append(url)
        return res

    def filterOnlineURLs(self,urls):
        """
        Filters a list of URLs for the ones that are accessible with this module
        """
        validurls=self.filterValidURLs(urls)
        res=[]
        for url in validurls:
            try:
                fh=urllib.urlopen(url)
                if fh.getcode()==200:
                    res.append(url)
                else:
                    pass
            except:
                pass
        return res


    def isURLOnline(self,url):
        """
        Checks if a URL of this file host is online
        """
        try:
            return (len(self.filterOnlineURLs([url]))>0)
        except:
            return false

    def isLoginValid(self,username,password):
        """
        Checks if the specified login credentials are valid
        """
        return True

    def isLoginForStreaming(self,username,password):
        """
        Checks if the supplied link is valid for streaming files within XBMC (think about free or expired accounts)
        """
        return True
    def login(self,username,password):
        """
        Logs into a file host service and stores cookie information for later use
        """ 
        return True

    def isLoggedIn(self):
        """
        Checks if the user is still logged in
        """
        return True
    
    def logout(self):
        """
        Logs out the currently logged in user.
        This deletes the login cookies.
        """
        return True

    def resolveURLs(self,urls):
        """
        Resolves a url for this module's host
        """
        return self.filterOnlineURLs(urls)

    def resolveURL(self,url):
        """
        Checks if the supplied link is valid for this file host
        """
        try:
            return self.filterOnlineURLs([url])[0]
        except:
            return None
    
    def findURLs(self,pagesource):
        """
        Finds URLs of this host within HTML page source
        """
        res=[]
        reres=re.findall(self.getRegularExpression(),pagesource)
        for oneurl in reres:
            try:
                res.append(oneurl[0])
            except:
                pass
        return res

    def findAndResolveURLs(self, pagesource):
        """
        Resolves all links found in the supplied HTML source to streamable URLs
        """
        r=self.findURLs(pagesource)
        return self.resolveURLs(r)

    def getFileName(self,url):
        """
        Returns the filename of a URL for this host (some do not store this in the URL)
        """
        try:
            return re.findall(r"/([\w_.-]*?(?=\?)|[\w_.-]*$/)",url)[0]
        except:
            return ""
        
    def getPlaylistItems(self,urls):
        """
        returns playlist items (resolved) for the specified urls. Adds all available meta info to it (icon, filename, etc.)
        """
        res=[]
        for url in urls:
            #create playlist item here
            pass
        return res
    
    def getPlaylistItem(self,url):
        """
        returns a playlist item (resolved) for the specified url. Adds all available meta info to it (icon, filename, etc.)
        """
        return self.getPlaylistItems([url])

