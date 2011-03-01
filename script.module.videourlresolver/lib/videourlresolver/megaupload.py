'''
Megaupload 1.0
Copyleft Anarchintosh.

Depends on mechanize module for login.
Could be hacked to remove this dependency.

Can also get megavideo links from megaupload pages.

Cut down from megaroutines, which will be rendered unneccessary by videoresolver.
Still needs to be tweaked a bit to remove unnecessary code.
'''

import sys,os,re
import urlparse,urllib,urllib2,cookielib
import mechanize

def openfile(filename):
     fh = open(filename, 'r')
     contents=fh.read()
     fh.close()
     return contents

def save(filename,contents):  
     fh = open(filename, 'w')
     fh.write(contents)  
     fh.close()

def checkurl(url):
   #get necessary url details
        ismegaup = re.search('.megaupload.com/', url)
        ismegavid = re.search('.megavideo.com/', url)
        isporn = re.search('.megaporn.com/', url)
   #second layer of porn url detection
        ispornvid = re.search('.megaporn.com/video/', url)
   # RETURN RESULTS:
        if ismegaup is not None:
           return 'megaup'
        elif ismegavid is not None:
           return 'megavid'
        elif isporn is not None:
           if ispornvid is not None:
              return 'pornvid'
           elif ispornvid is None:
              return 'pornup'

#set names of important files     
cookiefile='cookies.lwp' 


def get_dir(mypath, dirname):
    #...creates sub-directories if they are not found.
    subpath = os.path.join(mypath, dirname)
    if not os.path.exists(subpath):
        os.makedirs(subpath)
    return subpath

          
class megaupload:
   def __init__(self,path):
        self.class_name='megaupload'
        self.path = get_dir(path,'megaroutine_files')
        self.classpath = get_dir(self.path,self.class_name)
        self.cookie = os.path.join(self.classpath,cookiefile)

   def megavid_force(self,url,disable_cookies=True):
        source=self.load_pagesrc(url,disable_cookies)
        megavidlink=self.get_megavid(source)
        return megavidlink
      
   def resolve_megaup(self,url,aviget=False,force_megavid=False):

        #bring together all the functions into a simple user-friendly function.

        source=self.load_pagesrc(url)

        #if source is a url (from a Direct Downloads re-direct) not pagesource
        if source.startswith('http://'):
             filelink=source

             #can't get megavid link if using direct download, however, can load megaup page without cookies, then scrape.
             #this is time consuming, hence the force_megavid flag needed to enable it.
             if force_megavid is False:
                  megavidlink=None
             elif force_megavid is True:
                  megavidlink=self.megavid_force(url)

             #speed patch (we know its premium, since we're getting a direct download)
             logincheck='premium'

        else: # if source is html page code...

             #scrape the direct filelink from page
             filelink=self.get_filelink(source,aviget)

             #scrape the megavideo link if there is one on the page
             megavidlink=self.get_megavid(source)

             logincheck=self.check_login(source)

        filename=self._get_filename(filelink)
        
        return filelink,filename,megavidlink,logincheck


   def load_pagesrc(self,url,disable_cookies=False):
     
     #loads page source code. redirect url is returned if Direct Downloads is enabled.
        
     urltype=checkurl(url)
     if urltype is 'megaup' or 'megaporn':
          link=GetURL(url,self,disable_cookies)
          return link
     else:
          return False


   def check_login(self,source):
        #feed me some megaupload page source
        #returns 'free' or 'premium' if logged in
        #returns 'none' if not logged in
        
        login = re.search('<b>Welcome</b>', source)
        premium = re.search('flashvars.status = "premium";', source)        

        if login is not None:
             if premium is not None:
                  return 'premium'
             elif premium is None:
                  return 'free'
        elif login is None:
             return 'none'

 
   def dls_limited(self):
     #returns True if download limit has been reached.

     truestring='Download limit exceeded'
     falsestring='Hooray Download Success'   

     #url to a special small text file that contains the words: Hooray Download Success        
     testurl='http://www.megaupload.com/?d=PQCIEIP7'

     source=self.load_pagesrc(testurl)
     fileurl=self.get_filelink(source)

     link=GetURL(fileurl,self)

     exceeded = re.search(truestring, link)
     #notexceeded = re.search(falsestring, link)

     if exceeded is not None:
          return True
     else:
          #if notexceeded is not None:
               return False

   def delete_login(self):
     #clears cookies
     try:
          os.remove(self.cookie)
     except:
          pass
        
   def set_login(self,megauser=False,megapass=False):

          #refresh the cookies if successful
          login=Do_Login(self,megauser,megapass)

          #return whether login was successful
          return login
   
   def get_megavid ( self,source ):
        #verify source is megaupload 
        checker='<span class="down_txt3">Download link:</span> <a href="http://www.megaupload.com/'
        ismegaup=re.search(checker, source)

        if ismegaup is not None:
           #scrape for megavideo link (first check its there)
           megavidlink = re.search('View on Megavideo', source)
           if megavidlink is not None:
              megavidlink = re.compile('<a href="http://www.megavideo.(.+?)"').findall(source)
              megavid=megavidlink[0]
              megavid = 'http://www.megavideo.'+megavid
              return megavid
           if megavidlink is None:
              #no megavideo link on page
              return None
        if ismegaup is None:
           print 'not a megaupload url'
           return None


   def get_filelink(self,source,aviget=False):
          # load megaupload page and scrapes and adds videolink, passes through partname.  
          #print 'getting file link....'

          #try getting the premium link. if it returns none, use free link scraper.
          match1=re.compile('<a href="(.+?)" class="down_ad_butt1">').findall(source)
          if str(match1)=='[]':
               match2=re.compile('id="downloadlink"><a href="(.+?)" class=').findall(source)
               url=match2[0]
          else:
               url=match1[0]


          #aviget is an option where if a .divx file is found, it is renamed to .avi (necessary for XBMC)
          if aviget is True and url.endswith('divx'):
                    return url[:-4]+'avi'
          else:          
                    return url


   def _get_filename(self,url=False,source=False):
        #accept either source or url
        if url is False:
             if source is not False:
                  url=self.get_filelink(source)
        
        #get file name from url (ie my_vid.avi)
        name = re.split('\/+', url)
        return name[-1]

def Do_Login(self,megauser,megapass):

     try:
          os.remove(self.cookie)
     except:
          pass
     
     if megauser is not False or megapass is not False:
               # Browser
               br = mechanize.Browser()

               # Cookie Jar
               cj = cookielib.LWPCookieJar()
               br.set_cookiejar(cj)

               # Browser options
               br.set_handle_equiv(True)
               br.set_handle_gzip(True)
               br.set_handle_redirect(True)
               br.set_handle_referer(True)
               br.set_handle_robots(False)

               # Follows refresh 0 but not hangs on refresh > 0
               br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

               # User-Agent
               br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


               # The site we will navigate into, handling it's session
               if self.class_name is 'megaupload':
                    siteurl='http://www.megaupload.com/?c=login'

               elif self.class_name is 'megavideo':
                    siteurl='http://www.megavideo.com/?c=login'

               elif self.class_name is 'megaporn':
                    siteurl='http://www.megaporn.com/?c=login'

               elif self.class_name is 'megapornvid':
                    siteurl='http://www.megaporn.com/?c=login'
                    
               br.open(siteurl)
               

               # Select the first (index zero) form
               br.select_form('loginfrm')

               #User credentials
               br.form['username'] = megauser
               br.form['password'] = megapass
               br.submit()

               #check if login worked
               loginerror="Username and password do not match" in br.response().read()
               if loginerror == True:
                    return False
                    try:
                         os.remove(self.cookie)
                    except:
                         pass
               elif loginerror == False:
                    cj.save(self.cookie)
                    return True
                    

def GetURL(url,self=False,disable_cookies=False):
     #print 'processing url: '+url

     #logic to designate whether to handle cookies
     urltype=checkurl(url)
     if disable_cookies==False:
          if urltype is 'megaup' or 'megaporn' or 'megavid':
               if self is not False:
                    if os.path.exists(self.cookie):
                         use_cookie=True
                    else:
                         use_cookie=False  
               else:
                    use_cookie=False  
          else:
                    use_cookie=False  
     else:
          use_cookie=False

     # don't use cookie, if not logged in          
     if use_cookie is False:
          req = urllib2.Request(url)
          req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')       
          response = urllib2.urlopen(req)
          link=response.read()
          response.close()
          return link

     # use cookie, if logged in
     if use_cookie is True:
          cj = cookielib.LWPCookieJar()
          cj.load(self.cookie)
          req = urllib2.Request(url)
          req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')       
          opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
          response = opener.open(req)

          #check if we were redirected (megapremium Direct Downloads...)
          finalurl = response.geturl()
          if finalurl is url:
               link=response.read()
               response.close()
               return link
          elif finalurl is not url:
               #if we have been redirected, return the redirect url
               return finalurl
