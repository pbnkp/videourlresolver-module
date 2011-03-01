# -*- coding: UTF-8 -*-
import os, re, urllib2, logging
import utils.settings as settings

COOKIEFILE = os.path.join(os.getcwd(), 'cookies.lwp')

log = logging.getLogger("megavideo")
log.info("Cookiefile: %s" % COOKIEFILE)

def resolve(page):
  mega = re.compile('<param name="movie" value="http://www.megavideo.com/v/(.+?)">').findall(page)
  mega[0] = mega[0][0:8]
  megavideoUrl = __getUrl(mega[0])
  return [megavideoUrl]

#Coolblaze-xbmc forums.
def __ajoin(arr):
  strtest = ''
  for num in range(len(arr)):
    strtest = strtest + str(arr[num])
  return strtest

def __asplit(mystring):
  arr = []
  for num in range(len(mystring)):
    arr.append(mystring[num])
  return arr
    
def __decrypt(str1, key1, key2):
  __reg1 = []
  __reg3 = 0
  while (__reg3 < len(str1)):
    __reg0 = str1[__reg3]
    holder = __reg0
    if (holder == "0"):
      __reg1.append("0000")
    else:
      if (__reg0 == "1"):
        __reg1.append("0001")
      else:
        if (__reg0 == "2"): 
          __reg1.append("0010")
        else: 
          if (__reg0 == "3"):
            __reg1.append("0011")
          else: 
            if (__reg0 == "4"):
              __reg1.append("0100")
            else: 
              if (__reg0 == "5"):
                __reg1.append("0101")
              else: 
                if (__reg0 == "6"):
                  __reg1.append("0110")
                else: 
                  if (__reg0 == "7"):
                    __reg1.append("0111")
                  else: 
                    if (__reg0 == "8"):
                      __reg1.append("1000")
                    else: 
                      if (__reg0 == "9"):
                        __reg1.append("1001")
                      else: 
                        if (__reg0 == "a"):
                          __reg1.append("1010")
                        else: 
                          if (__reg0 == "b"):
                            __reg1.append("1011")
                          else: 
                            if (__reg0 == "c"):
                              __reg1.append("1100")
                            else: 
                              if (__reg0 == "d"):
                                __reg1.append("1101")
                              else: 
                                if (__reg0 == "e"):
                                  __reg1.append("1110")
                                else: 
                                  if (__reg0 == "f"):
                                    __reg1.append("1111")

    __reg3 = __reg3 + 1

  mtstr = __ajoin(__reg1)
  __reg1 = __asplit(mtstr)
  __reg6 = []
  __reg3 = 0
  while (__reg3 < 384):
  
    key1 = (int(key1) * 11 + 77213) % 81371
    key2 = (int(key2) * 17 + 92717) % 192811
    __reg6.append((int(key1) + int(key2)) % 128)
    __reg3 = __reg3 + 1
  
  __reg3 = 256
  while (__reg3 >= 0):

    __reg5 = __reg6[__reg3]
    __reg4 = __reg3 % 128
    __reg8 = __reg1[__reg5]
    __reg1[__reg5] = __reg1[__reg4]
    __reg1[__reg4] = __reg8
    __reg3 = __reg3 - 1
  
  __reg3 = 0
  while (__reg3 < 128):
  
    __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
    __reg3 = __reg3 + 1

  __reg12 = __ajoin(__reg1)
  __reg7 = []
  __reg3 = 0
  while (__reg3 < len(__reg12)):

    __reg9 = __reg12[__reg3:__reg3 + 4]
    __reg7.append(__reg9)
    __reg3 = __reg3 + 4
    
  
  __reg2 = []
  __reg3 = 0
  while (__reg3 < len(__reg7)):
    __reg0 = __reg7[__reg3]
    holder2 = __reg0
  
    if (holder2 == "0000"):
      __reg2.append("0")
    else: 
      if (__reg0 == "0001"):
        __reg2.append("1")
      else: 
        if (__reg0 == "0010"):
          __reg2.append("2")
        else: 
          if (__reg0 == "0011"):
            __reg2.append("3")
          else: 
            if (__reg0 == "0100"):
              __reg2.append("4")
            else: 
              if (__reg0 == "0101"): 
                __reg2.append("5")
              else: 
                if (__reg0 == "0110"): 
                  __reg2.append("6")
                else: 
                  if (__reg0 == "0111"): 
                    __reg2.append("7")
                  else: 
                    if (__reg0 == "1000"): 
                      __reg2.append("8")
                    else: 
                      if (__reg0 == "1001"): 
                        __reg2.append("9")
                      else: 
                        if (__reg0 == "1010"): 
                          __reg2.append("a")
                        else: 
                          if (__reg0 == "1011"): 
                            __reg2.append("b")
                          else: 
                            if (__reg0 == "1100"): 
                              __reg2.append("c")
                            else: 
                              if (__reg0 == "1101"): 
                                __reg2.append("d")
                              else: 
                                if (__reg0 == "1110"): 
                                  __reg2.append("e")
                                else: 
                                  if (__reg0 == "1111"): 
                                    __reg2.append("f")
                                  
    __reg3 = __reg3 + 1

  endstr = __ajoin(__reg2)
  return endstr

def __getUrl(mega):
  if settings.isSet("megavideopremium"):
    return __getPremiumUrl(mega)
  else:
    return __getPublicUrl(mega)
  
def __getPremiumUrl(code):
  log.debug("Use premium mode")
  megavideologin = settings.get("megavideouser")
  log.debug("Megavideo Username: '%s'" % megavideologin)
  megavideopassword = settings.get("megavideopassword")
  #log.debug("megavideopassword=#"+megavideopassword+"#")
  megavideocookie = __getMegavideoUserCookie(megavideologin, megavideopassword)
  log.debug("Megavideo cookie: '%s'" % megavideocookie)
  req = urllib2.Request("http://www.megavideo.com/xml/player_login.php?u=" + megavideocookie + "&v=" + code)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  patronvideos = 'downloadurl="([^"]+)"'
  matches = re.compile(patronvideos, re.DOTALL).findall(urllib2.urlopen(req).read())
  return matches[0].replace("%3A", ":").replace("%2F", "/").replace("%20", " ")
  
def __getPublicUrl(code):
  log.debug("Use normal mode")
  req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v=" + code)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
  req.add_header('Referer', 'http://www.megavideo.com/')
  page = urllib2.urlopen(req);response = page.read();page.close()
  errort = re.compile(' errortext="(.+?)"').findall(response)
  if len(errort) <= 0:
    s = re.compile(' s="(.+?)"').findall(response)
    k1 = re.compile(' k1="(.+?)"').findall(response)
    k2 = re.compile(' k2="(.+?)"').findall(response)
    un = re.compile(' un="(.+?)"').findall(response)
  return "http://www" + s[0] + ".megavideo.com/files/" + __decrypt(un[0], k1[0], k2[0]) + "/?.flv"
  
def __getMegavideoUserCookie(login, password):
  log.debug("getMegavideoUserCookie")
  ficherocookies = COOKIEFILE
  cj = None
  ClientCookie = None
  cookielib = None

  try:
    import cookielib
  except ImportError:
    try:
      import ClientCookie
    except ImportError:
      urlopen = urllib2.urlopen
      Request = urllib2.Request
    else:
      urlopen = ClientCookie.urlopen
      Request = ClientCookie.Request
      cj = ClientCookie.LWPCookieJar()
  else:
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()

  if cj is not None:
    if os.path.isfile(ficherocookies):
      cj.load(ficherocookies)

    if cookielib is not None:
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
      urllib2.install_opener(opener)

    else:
      opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
      ClientCookie.install_opener(opener)

  url = "http://www.megavideo.com/?s=signup"
  theurl = url
  # an example url that sets a cookie,
  # try different urls here and see the cookie collection you can make !
  txdata = "action=login&cnext=&snext=&touser=&user=&nickname=" + login + "&password=" + password
  txheaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
          'Referer':'http://www.megavideo.com/?s=signup'}
  req = Request(theurl, txdata, txheaders)
  handle = urlopen(req)
  cj.save(ficherocookies)                     # save the cookies again    

  handle.read()
  data = handle.read()
  log.debug("----------------------")
  log.debug("Respuesta de getUrl")
  log.debug("----------------------")
  log.debug(data)
  log.debug("----------------------")
  handle.close()

  cookiedatafile = open(ficherocookies, 'r')
  cookiedata = cookiedatafile.read()
  cookiedatafile.close();

  log.debug("----------------------")
  log.debug("Cookies despues")
  log.debug("----------------------")
  log.debug(cookiedata)
  log.debug("----------------------")

  patronvideos = 'user="([^"]+)"'
  matches = re.compile(patronvideos, re.DOTALL).findall(cookiedata)
  if len(matches) == 0:
    patronvideos = 'user=([^\;]+);'
    matches = re.compile(patronvideos, re.DOTALL).findall(cookiedata)
    
  return matches[0]
