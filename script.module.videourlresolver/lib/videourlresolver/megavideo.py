# -*- coding: UTF-8 -*-

"""
 Megavideo and Megaporn-Video Resolver 0.1
 Copyleft Anarchintosh 

 This resolver is based on work from Ksosez, Pedro Guedes, Voinage and Coolblaze.

 If anyone gets the time, please update with code from http://code.google.com/p/python-megavideo-parser/

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
import urllib,urllib2,cookielib
import logging
log = logging.getLogger("megavideo")


def openfile(filepath):
     fh = open(filepath, 'r')
     contents=fh.read()
     fh.close()
     return contents

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



  
    return __GetCookie(baseurl, cookiepath, myuser, mypass)
  else:
    return None

def check_login(source):
        #feed me some mega page source
        #returns 'free' or 'premium' if logged in
        #returns 'none' if not logged in
        
        login = re.search('<b>Welcome</b>', source)
        premium = re.search('flashvars.status = "premium";', source)        

        if login is not None:
             if premium is not None:
                  return 'premium'
             elif premium is None:
                  return 'free'
        else:
             return login
          
def __doLogin(baseurl, cookiepath, username, password):

    if username and password:
        #delete the old cookie
        try:
              os.remove(cookiepath)
        except:
              pass

        #build the login code, from user, pass, baseurl and cookie
        login_data = urllib.urlencode({'username' : username, 'password' : password, 'login' : 1, 'redir' : 1})   
        req = urllib2.Request(baseurl + '?c=login', login_data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #do the login and get the response
        response = response.read(opener.open(req))

        login = check_login(response)

        if login == 'free' or login == 'premium':
            cj.save(cookiepath)

        return login
    else:
         return None
  
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
