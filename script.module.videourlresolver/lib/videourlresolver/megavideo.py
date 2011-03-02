# -*- coding: UTF-8 -*-

"""
 Megavideo and Megaporn-Video Resolver 0.1
 Anarchintosh Copyleft

 This resolver is based on work from Ksosez, Pedro Guedes, Voinage and Coolblaze.

 Commands:
 
 __doLogin(baseurl, cookiepath, username, password)

 __getPremiumUrl(baseurl, cookiepath, code)

 __getPublicUrl(baseurl, cookiepath, code)
 (in __getPublicUrl, None is a valid setting for cookiepath)

"""

#global strings for valid baseurl
porn = 'http://www.megaporn.com/video/'
regular = 'http://www.megavideo.com/'

import os,re
import urllib2,cookielib
import mechanize
import logging
log = logging.getLogger("megavideo")


def openfile(filepath):
     fh = open(filepath, 'r')
     contents=fh.read()
     fh.close()
     return contents
    
def __doLogin(baseurl, cookiepath, myuser, mypass):

  if myuser and mypass:
    return __new_GetCookie(baseurl, cookiepath, myuser, mypass)
  else:
    return None

def __calcDecriptionMix(hash, keyMix):
  """Mixes the decription keys into the hash and returns the updated hash
  @param hash: the hash to merge the keys into
  @param keyMix: the array of keys to mix"""
  for i in range(128):
    hash[i] = str(int(hash[i]) ^ int(keyMix[i + 256]) & 1)
  return "".join(hash)

def __toHexDecriptionString(binaryChunks):
  """Converts an array of binary strings into a string of the corresponding hex chunks merged
  This method will first loop through the binary strings converting each one into it's correspondent
  hexadecimal string and then merge the resulting array into a string
  @param binaryChunks: an array of binary strings
  @return: a string of the corresponding hexadecimal strings, merged"""
  hexChunks = []
  for binChunk in binaryChunks:
    hexChunks.append("%x" % int(binChunk, 2))    
  return "".join(hexChunks)

def __doDecriptionChunks(binaryMergedString):
  """Break a string of 0's and 1's in pieces of 4 chars
  @param binaryMergedString: a string of 0's and 1's to break in 4-part pieces
  @return: an array of 4 character parts of the original string"""
  binaryChunks = []
  for index in range(0, len(binaryMergedString), 4):
    binaryChunk = binaryMergedString[index:index + 4]
    binaryChunks.append(binaryChunk)
  return binaryChunks

def __doDecriptionSwaps(hash, keys):
  """Swap the first 256 indices from keys on the hash with the last 128 elements from the hash
  @param hash: the hash to do swaps on
  @param keys: the generated keys to use as indices for the swaps
  @return: hash after swaps"""
  for index in range(256, 0, -1):
    key = keys[index]
    swapTarget = index % 128
    oldHashKey = hash[key]
    hash[key] = hash[swapTarget]
    hash[swapTarget] = oldHashKey
  return hash

def __computeIndices(key1, key2):
  """Generate an array of 384 indices with values 0-127
  @param key1: first seed to generate indices from
  @param key2: second seed to generate indices from
  @return: an array of 384 indices with values between 0 and 127"""
  indices = []
  for i in range(384):
    key1 = (int(key1) * 11 + 77213) % 81371
    key2 = (int(key2) * 17 + 92717) % 192811
    indices.append((int(key1) + int(key2)) % 128)
  return indices

def __explodeBin(str1):
  # explode each char in str1 into it;s binary representation
  # and collect the result into __reg1
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
  return list("".join(__reg1))
    
def __calculateFileHash(str1, key1, key2):
  # explode hex to bin strings, collapse to a string and return char array
  hash = __explodeBin(str1)
  # based on the keys, generate an array of 384 (256 + 128) values
  decriptIndices = __computeIndices(key1, key2)
  # from 256 to 0, swap hash[decriptIndices[x]] with hash[__reg3 % 128]
  hash = __doDecriptionSwaps(hash, decriptIndices)
  # replace the first 128 chars in hash with the formula:
  #  hash[x] = hash[x] * decriptIndices[x+256] & 1
  hash = __calcDecriptionMix(hash, decriptIndices)
  # split __reg12 in chunks of 4 chars
  chunks = __doDecriptionChunks(hash)  
  # convert each binary chunk to a hex string for the final hash
  return __toHexDecriptionString(chunks)

  
def __getPremiumUrl(baseurl, cookiepath, code):

  login_code = (re.compile("user=(.+?)\;").findall(openfile(cookiepath)))[0]
  
  log.debug("Use premium mode")
  log.debug("Megavideo cookie: '%s'" % login_code)
  req = urllib2.Request(baseurl + "xml/player_login.php?u=" + login_code + "&v=" + code)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  patronvideos = 'downloadurl="([^"]+)"'
  matches = re.compile(patronvideos, re.DOTALL).findall(urllib2.urlopen(req).read())
  return [matches[0].replace("%3A", ":").replace("%2F", "/").replace("%20", " ")]
  
def __getPublicUrl(baseurl, cookiepath, code):

  if cookiepath is not None:

    login_code = (re.compile("user=(.+?)\;").findall(openfile(cookiepath)))[0]

    log.debug("Mega cookie: '%s'" % login_code)
    url = baseurl + "xml/videolink.php?u=" + login_code + "&v=" + code

  else:
    log.debug("Use normal mode")
    url = baseurl + "xml/videolink.php?v=" + code
    
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
  req.add_header('Referer', baseurl)
  page = urllib2.urlopen(req);response = page.read();page.close()
  print page
  errort = re.compile(' errortext="(.+?)"').findall(response)
  if len(errort) <= 0:
    s = re.compile(' s="(.+?)"').findall(response)
    k1 = re.compile(' k1="(.+?)"').findall(response)
    k2 = re.compile(' k2="(.+?)"').findall(response)
    un = re.compile(' un="(.+?)"').findall(response)
    
    return ["http://www" + s[0] + baseurl[10:25] + "files/" + __calculateFileHash(un[0], k1[0], k2[0]) + "/?.flv"]

def __new_GetCookie(baseurl, cookiepath, megauser, megapass):

     try:
          os.remove(cookiepath)
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
               login_url = baseurl + '?c=login'
               br.open(login_url)
               

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
                         os.remove(cookiepath)
                    except:
                         pass
               elif loginerror == False:
                    cj.save(cookiepath)
                    return True

def __old_GetCookie(baseurl, cookiepath, login, password):

  log.debug("getCookie")
  ficherocookies = cookiepath

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

  signup_url = baseurl+"?s=signup"
  
  txdata = "action=login&cnext=&snext=&touser=&user=&nickname=" + login + "&password=" + password
  txheaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
          'Referer': signup_url}
  req = Request(signup_url, txdata, txheaders)

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

  cookiedata = openfile(ficherocookies)

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
