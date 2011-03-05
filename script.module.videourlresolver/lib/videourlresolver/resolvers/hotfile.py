
import hashlib, urllib, urllib2, filehostmodule, os, re

class HotFileModule(filehostmodule.FileHostModule):
	
	def __init__(self):
		self.username=""
		self.password=""
	
	def __hotfileapicall(self, action, user, pas, params):
				md5mod=hashlib.md5()
				md5mod.update(pas)
				pwmd5 = md5mod.hexdigest()
				url = 'http://api.hotfile.com/'
				data = {'action': action, 'username': user, 'passwordmd5': pwmd5}
				for par in params:
					data[par] = params[par]
				data = urllib.urlencode(data)
				req = urllib2.Request(url + "?" + data)
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
				response = urllib2.urlopen(req)
				return response.read()
	
	def __getHFLink(self, user, pas, url):
		return self.__hotfileapicall("getdirectdownloadlink", user, pas, {"link":url})
		
	def __getHFLinks(self, user, pas, urls):
		return self.__hotfileapicall("getdirectdownloadlinks", user, pas, {"links":",".join(urls)})

	def __checkHFLinks(self, user, pas, urls):
		resp=self.__hotfileapicall("checklinks", user, pas, {"fields":"status","links":",".join(urls)})
		resparray=resp.split()
		retlinks=[]
		for i in range(0,len(urls)-1):
			if resparray[i][0]=="1":
				retlinks.append(urls[i])
		return retlinks

	def getIconFileHost(self):
		return os.path.join(__file__, "resolver_icons", "hotfile.png")
	
	def getRegularExpression(self):
		return r"http://(www.)?hotfile\.com/dl/\d+/[0-9a-zA-Z]+/"
	
	def filterOnlineURLs(self, urls):
		validurls = self.filterValidURLs(urls)
		return self.__checkHFLinks(self.username,self.password,validurls)

	def isLoginValid(self, username, password):
		return not self.__hotfileapicall("getuserinfo",username,password,[])==".invalid username or password"

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
			cols=line.split("|")
			if cols[0]!="":
				if cols[1][0:4]=="http":
					ret.append(cols[1])
		return ret

	def getFileName(self, url):
		res=self.__getHFLinks(self.username,self.password,urls)
		cols=res.replace("\n","").split("|")
		if cols[0]!="":
			if cols[1][0:4]=="http":
				return cols[0]
		return None
		
bla = HotFileModule()
print bla.login("torbeng", "hagentest")
urls=["http://hotfile.com/dl/108674985/fb8ae70/the.colbert.report.2011.03.03.mark.w.moffett.hdtv.xvid-lmao.avi.html","http://hotfile.com/dl/12/332/","http://hotfile.com/dl/108674446/7daa5bf/the.colbert.report.2011.03.03.mark.w.moffett.hdtv.xvid-lmao.avi.html","http://hotfile.com/dl/107020153/77419c0/Plants.vs.Zombies.1.025.MacOSX-P2P.zip.html","http://hotfile.com/dl/104509869/f57718c/"]
print bla.filterOnlineURLs(urls)
print bla.resolveURLs(urls)
print bla.getFileName(urls[0])